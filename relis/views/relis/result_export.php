<?php

$python_environment_filename = FCPATH . "cside/export_python/python_env_" . project_db() . ".zip";

if (file_exists($python_environment_filename)) {
    $paper_size = (filesize($python_environment_filename) > 1000 ? round(filesize($python_environment_filename) / 1000) : round(filesize($python_environment_filename) / 1000, 1)) . ' Kb  Last update:';
    $paper_date = date("Y-m-d h:i:s", filemtime($python_environment_filename));

    $python_environment_dsc = "<i class='fa fa-download'></i> Download Python (" . $paper_size . $paper_date . ")";
} else {

    $python_environment_dsc = "";
}
?>

<tr>
    <td>Python environment</td>
    <td><a href="<?php echo base_url(); ?>reporting/python_download/python_env_<?php echo project_db(); ?>.zip"><?php echo $python_environment_dsc ?></a></td>
    <td><a href="<?php echo base_url(); ?>reporting/python_environment_export"><i class="fa fa-refresh"></i><?php echo lng('Update file') ?></a></td>
</tr>