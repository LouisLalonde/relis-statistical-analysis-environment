<?php
class Reporting extends CI_Controller
{
    /**
     * Functions which are used to perform the statistical
     * analysis of a given project
     */
    private function python_statistical_functions()
    {
        return array(
            $this->python_statistical_function_factory(
                'desc_frequency_table',
                'Frequency tables',
                'descriptive',
                'Nominal',
                'Dataframe'
            ),
            $this->python_statistical_function_factory(
                'desc_bar_plot',
                'Bar plots',
                'descriptive',
                'Nominal',
                'Figure'
            ),
            $this->python_statistical_function_factory(
                'desc_statistics',
                'Statistics',
                'descriptive',
                'Continuous',
                'Dataframe'
            ),
            $this->python_statistical_function_factory(
                'desc_box_plot',
                'Box plots',
                'descriptive',
                'Continuous',
                'Figure'
            ),
            $this->python_statistical_function_factory(
                'desc_violin_plot',
                'Violin plots',
                'descriptive',
                'Continuous',
                'Figure'
            ),
            $this->python_statistical_function_factory(
                'evo_frequency_table',
                'Frequency tables',
                'evolutive',
                'Nominal',
                'Dataframe'
            ),
            $this->python_statistical_function_factory(
                'evo_plot',
                'Evolution plots',
                'evolutive',
                'Nominal',
                'Figure'
            ),
            $this->python_statistical_function_factory(
                'comp_frequency_table',
                'Frequency tables',
                'comparative',
                'Nominal',
                'Dataframe'
            ),
            $this->python_statistical_function_factory(
                'comp_stacked_bar_plot',
                'Stacked bar plots',
                'comparative',
                'Nominal',
                'Figure'
            ),
            $this->python_statistical_function_factory(
                'comp_grouped_bar_plot',
                'Grouped bar plots',
                'comparative',
                'Nominal',
                'Figure'
            ),
            $this->python_statistical_function_factory(
                'comp_bubble_chart',
                'Bubble charts',
                'comparative',
                'Nominal',
                'Figure'
            ),
            $this->python_statistical_function_factory(
                'comp_chi_squared_test',
                'Chi-squared test',
                'comparative',
                'Nominal',
                'Dataframe'
            ),
            $this->python_statistical_function_factory(
                'comp_shapiro_wilk_test',
                'Shapiro Wilk\'s correlation test',
                'descriptive',
                'Continuous',
                'Dataframe'
            ),
            $this->python_statistical_function_factory(
                'comp_pearson_cor_test',
                'Pearson\'s correlation test',
                'comparative',
                'Continuous',
                'Dataframe'
            ),
            $this->python_statistical_function_factory(
                'comp_spearman_cor_test',
                'Spearman\'s correlation test',
                'comparative',
                'Continuous',
                'Dataframe'
            )
        );
    }

    /**
     * Abstract the creation of statistics for the analysis of classfication data
     */
    private function python_statistical_function_factory(
        $name,
        $title,
        $type,
        $data_type,
        $return_type
    ) {
        return array(
            'name' => $name,
            'title' => $title,
            'type' => $type,
            'data_type' => $data_type,
            'return_data_type' => $return_type,
        );
    }

    /**
     * Deletes obsolete fields from the classification data
     */
    private function python_fields_cleaning($table_fields, $classification_metadata_fields)
    {
        foreach ($classification_metadata_fields as $field_key) {
            if (array_key_exists($field_key, $table_fields)) {
                unset($table_fields[$field_key]);
            }
        }
        unset($field_value);
        return $table_fields;
    }

    /**
     * Evaluate the cardinality of a field's value.s
     */
    private function python_evaluate_multiple($field_size)
    {
        if ($field_size > 1) {
            return true;
        }
        return false;
    }

    /**
     * Taken from the r_export_configurations view
     * 
     * Evaluates the data type of a field.
     * No value is returned if the type
     * isn't equal to Nominal or Continuous
     */
    private function python_evaluate_field_type_condition($value)
    {
        if (
            ($value['field_type'] === 'text' && $value['category_type'] != 'FreeCategory') ||
            ($value['field_type'] === 'int' && $value['category_type'] != 'FreeCategory') ||
            ($value['field_type'] === 'int' && $value['category_type'] === 'FreeCategory' &&
                $value['input_type'] === 'select')
        ) {
            return 'Nominal';
        } elseif (
            ($value['field_type'] === 'int' || $value['field_type'] === 'real') &&
            $value['category_type'] === 'FreeCategory' &&
            $value['input_type'] != 'select'
        ) {
            return 'Continuous';
        }
    }

    /**
     * Returns the set of statistical functions associated to a given field in terms
     * of it's data_type
     */
    private function python_evaluate_field_statistical_functions($field_type, $statistical_functions)
    {
        $field_statistical_functions = array_filter($statistical_functions, function ($statistical_function) use ($field_type) {
            return $statistical_function['data_type'] == $field_type;
        });

        // Reset the indexes
        return array_values($field_statistical_functions);
    }

    /**
     * Abstract the creation of statistical classification fields 
     */
    private function python_statistical_classification_field_factory(
        $field_name,
        $field_title,
        $field_type,
        $multiple,
        $statistical_functions
    ) {
        return array(
            'name' => $field_name, 'title' => $field_title,
            'data_type' => $field_type, 'multiple' => $multiple, 'statistics' => $statistical_functions
        );
    }

    /**
     * Update and extend the results object with new field data:
     * Field title
     * Field type
     * Field is multiple
     */
    private function python_statistical_analysis_model_factory($table_fields, $statistical_functions)
    {
        foreach ($table_fields as $field_name => &$field_value) {
            $type = $this->python_evaluate_field_type_condition($field_value);

            // Removing the classification field if the type is unknown
            if (empty($type)) {
                unset($table_fields[$field_name]);
                continue;
            }

            $field_statistical_functions = $this->python_evaluate_field_statistical_functions(
                $type,
                $statistical_functions
            );
            $multiple = $this->python_evaluate_multiple($field_value['number_of_values']);
            $table_fields[$field_name] = $this->python_statistical_classification_field_factory(
                $field_name,
                $field_value['field_title'],
                $type,
                $multiple,
                $field_statistical_functions
            );
        }
        return $table_fields;
    }

    /**
     * Add mandatory fields which are shared between projects to the final data structure 
     */
    private function python_add_static_classification_fields($results, $classification_static_fields)
    {
        foreach ($classification_static_fields as $field_name => &$field_value) {
            if (!array_key_exists($field_name, $results)) {
                $results[$field_name] = $field_value;
            }
        }
        return $results;
    }

    /**
     * Extract the classification configuration of a given project
     */
    private function python_extract_classification_configuration()
    {
        $table_ref = "classification";

        $this->db2 = $this->load->database(project_db(), TRUE);
        $ref_table_config = get_table_config($table_ref);
        return $ref_table_config['fields'];
    }

    /**
     * Creates the project statistical analysis model which conforms
     * to the relis-statistical-analysis-dsl metamodel
     */
    private function python_create_statistical_analysis_model(
        $classification_configuration,
        $export_config
    ) {
        $results = $this->python_fields_cleaning(
            $classification_configuration,
            $export_config['CLASSIFICATION_METADATA_FIELDS']
        );
        $results = $this->python_add_static_classification_fields(
            $results,
            $export_config['CLASSIFICATION_STATIC_FIELDS']
        );
        $sam = $this->python_statistical_analysis_model_factory(
            $results,
            $export_config['STATISTICAL_FUNCTIONS']
        );

        return $sam;
    }

    /**
     * Encapsulate static and dynaminc configuration parameters related
     * to the relis-statistical-analysis-environment
     */
    private function python_create_export_config($statistical_functions)
    {
        $PROJECT_NAME = project_db();
        $CLASSIFICATION_METADATA_FIELDS = array(
            'class_active', 'class_id',
            'class_paper_id', 'classification_time', 'user_id', 'A_id'
        );
        $CLASSIFICATION_STATIC_FIELDS = array(
            'publication_year' => array(
                'field_title' => 'Publication year',
                'field_type' => 'int',
                'number_of_values' => '1',
                'category_type' => 'FreeCategory',
                'input_type' => 'text'
            )
        );
        $MULTIVALUE_SEPARATOR = '|';
        $DROP_NA = false;
        $TARGET_DIRECTORY = 'cside/export_python/';
        $CLASSIFICATION_FILE_NAME = 'relis_classification_' . $PROJECT_NAME . '.csv';

        return array(
            'PROJECT_NAME' => $PROJECT_NAME,
            'CLASSIFICATION_METADATA_FIELDS' => $CLASSIFICATION_METADATA_FIELDS,
            'CLASSIFICATION_STATIC_FIELDS' => $CLASSIFICATION_STATIC_FIELDS,
            'MULTIVALUE_SEPARATOR' => $MULTIVALUE_SEPARATOR,
            'DROP_NA' => $DROP_NA,
            'STATISTICAL_FUNCTIONS' => $statistical_functions,
            'TARGET_DIRECTORY' => $TARGET_DIRECTORY,
            'CLASSIFICATION_FILE_NAME' => $CLASSIFICATION_FILE_NAME
        );
    }

    /**
     * Package the environment into a zip file
     */
    private function python_compress_executable_artifacts(
        $library_artifact_name,
        $playground_artifact_name,
        $python_kernel,
        $python_playground,
        $project_name,
        $target_directory,
        $classification_file_name
    ) {
        $zip = new ZipArchive();

        $python_env_name = 'python_env_' . $project_name;
        $zip_file_name = $target_directory . $python_env_name . '.zip';
        $requirements_file_name = 'requirements.txt';

        if ($zip->open($zip_file_name, ZipArchive::CREATE) !== TRUE) {
            throw new Exception('Cannot open ' . $zip_file_name);
        }

        $zip->addFromString($library_artifact_name, $python_kernel);
        $zip->addFromString($playground_artifact_name, $python_playground);
        $zip->addFile('cside/export_r/' . $classification_file_name, $classification_file_name);
        $zip->addFile('cside/python_templates/' . $requirements_file_name, $requirements_file_name);

        $zip->close();
    }

    private function python_create_twig_setup()
    {
        // Initial setup for TWIG 
        require_once 'vendor/autoload.php';

        $loader = new \Twig\Loader\FilesystemLoader('cside/python_templates');
        $twig = new \Twig\Environment($loader, [
            'cache' => false
        ]);

        return $twig;
    }

    /**
     * TWIG static configuration parameters
     */
    private function python_create_twig_config()
    {
        return array(
            'LIBRARY_ARTIFACT_NAME' => 'relis_statistics_kernel.py',
            'PLAYGROUND_ARTIFACT_NAME' => 'relis_statistics_playground.py'
        );
    }

    /**
     * Function that uses the TWIG templates engine to generate the python
     * artifacts part of the relis-statistical-analysis-environment
     */
    private function python_twig_generate(
        $sam,
        $artifact_name,
        $export_config,
        $twig_setup
    ) {
        try {
            return $twig_setup->render($artifact_name, array(
                'sam' => $sam,
                'export_config' => $export_config
            ));
        } catch (Exception $e) {
            set_top_msg($e);
        }
    }

    /**
     * Orchestrator for the python statistical analysis environment
     * generation
     */
    public function python_environment_export()
    {
        try {
            # Project classification configuration extraction
            $classification_configuration = $this->python_extract_classification_configuration();

            # Project statistical analysis modelization
            $statistical_functions = $this->python_statistical_functions();
            $export_config = $this->python_create_export_config($statistical_functions);
            $sam = $this->python_create_statistical_analysis_model(
                $classification_configuration,
                $export_config
            );

            # Generate/update project classification data
            $this->generate_result_export_classification();

            # Environment code generation
            $twig_setup = $this->python_create_twig_setup();
            $twig_config = $this->python_create_twig_config();

            $python_kernel_artifact = $this->python_twig_generate(
                $sam,
                $twig_config['LIBRARY_ARTIFACT_NAME'],
                $export_config,
                $twig_setup
            );

            $python_playground_artifact = $this->python_twig_generate(
                $sam,
                $twig_config['PLAYGROUND_ARTIFACT_NAME'],
                $export_config,
                $twig_setup
            );

            $twig_config = $this->python_create_twig_config();

            # Environment packaging
            $this->python_compress_executable_artifacts(
                $twig_config['LIBRARY_ARTIFACT_NAME'],
                $twig_config['PLAYGROUND_ARTIFACT_NAME'],
                $python_kernel_artifact,
                $python_playground_artifact,
                $export_config['PROJECT_NAME'],
                $export_config['TARGET_DIRECTORY'],
                $export_config['CLASSIFICATION_FILE_NAME']
            );

            set_top_msg(lng_min('Python environment generated'));

            redirect('reporting/result_export');
        } catch (Exception $e) {
            set_top_msg($e);
        }
    }

    /**
     * Extended from the download file function
     * Both functions could be generalized into
     * a single one 
     */
    public function python_download($file_name)
    {
        $url = "cside/export_python/" . $file_name;
        header("Content-Type: application/zip");
        header("Content-Transfer-Encoding: Binary");
        header("Content-disposition: attachment; filename=\"" . $file_name . "\"");
        readfile($url);
    }
}

?>
