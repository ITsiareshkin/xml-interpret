<?php
    /*      IPP 2 (test.php)
    *  Ivan Tsiareshkin (xtsiar00)
    *  19.04.2022
    */

    function print_head() {
        // Print html start
        echo '<!DOCTYPE html><html>';
        echo '
            <head>
                <meta http-equiv="Content-Type" content="text/html; charset=utf-8" />
                <title> IPP TEST.PHP </title>
            <head>
            ';

        // Print header, important to have gigachad (gains) background color
        echo '
            <body style="background-color:GAINSboro;">
            <h1 style="color:DimGray;font-family:courier;font-size:22px;">
                IPP - Principles of Programming Languages
            </h1>
            ';

        // Print table head
        echo '
            <table style="width:100%;border:line;border-collapse: collapse;">
                <thead>
                    <tr style="background-color:DimGray;color:white;font-family:courier;font-size:21px;text-align:left;border-collapse:collapse">
                        <th>Number</th>
                        <th>Path</th>
                        <th>Test name</th>
                        <th>Expected retval</th>
                        <th>Current retval</th>
                        <th>Output</th>
                        <th>Status</th>
                    </tr>
                </thead>
                <tbody>
            ';
    }

    // Print 1 table line with all info with test results
    function print_body($test_counter, $path, $test_name, $expected_retval, $exit_code, $out, $status) {
        if ($status == "OK") {
            echo '
            <tr style="background-color:lightgreen;color:black;font-family:courier;text-align:left;border-collapse:collapse">';
        } else
        if ($status == "FAIL") {
            echo '
            <tr style="background-color:#FF6150;color:black;font-family:courier;text-align:left;border-collapse:collapse">';
        }
        echo "
                <td>$test_counter</td>
                <td>$path</td>
                <td>$test_name</td>
                <td>$expected_retval</td>
                <td>$exit_code</td>
                <td>$out</td>
                <td>$status</td>
            </tr>
            ";
    }

    // Pring tests summary with percentage of passed tests
    function print_summary($test_counter, $passed_tests, $failed_tests) {
        $percentage = round((($passed_tests * 100) / $test_counter), 1, PHP_ROUND_HALF_DOWN);

        if ($percentage > 69) {
            echo "<span style='background-color:DimGray;color:white;font-size: 22px;font-family:courier;'> <b>Tests success rate:</b></span>";
            echo "<span style='color:green;font-size:22px;font-family:courier;'> $percentage"."%</span><br><br>";
        } else
        if ($percentage < 70 and $percentage > 20) {
            echo "<span style='background-color:DimGray;color:white;font-size: 22px;font-family:courier;'> <b>Tests success rate:</b></span>";
            echo "<span style='color:orange;font-size: 22px;font-family:courier;'> $percentage"."%</span><br><br>";
        } else
        if ($percentage < 21 and $percentage >= 0) {
            echo "<span style='background-color:DimGray;color:white;font-size: 22px;font-family:courier;'> <b>Tests success rate:</b></span>";
            echo "<span style='color:red;font-size: 22px;font-family:courier;'> $percentage"."%</span><br><br>";
        }

        echo "
            <span style='color:DimGray;font-size: 20px;font-family:courier;'>Total : "."$test_counter</span><br>
            <span style='color:DimGray;font-size: 20px;font-family:courier;'>Passed: "."$passed_tests</span><br>
            <span style='color:DimGray;font-size: 20px;font-family:courier;'>Failed: "."$failed_tests</span><br><br>
            ";
    }

    // Pring html end
    function print_end() {
        echo '
                </table>
            </body>
        </html>
            ';
    }

    ini_set("display_errors", "stderr");

    // Default values
    $dir = "./";
    $parse_script = "./parse.php";
    $int_script = "./interpret.py";
    $parse_only = false;
    $int_only = false;
    $recursive = false;
    $jexampath = "/pub/courses/ipp/jexamxml/";
    $noclean = false;

    // Possible args
    $opts = array("help", "directory:", "recursive", "parse-script:", "int-script:", "parse-only", "int-only", "jexampath:", "noclean");
    $args = getopt("", $opts);
    if (array_key_exists("help",$args)) {
        if($argc == 2) {
            echo "Test script for testing parser and IPPcode22 code interpreter\n";
            echo "Usage: test.php [options]\n\n";
            echo "options:\n";
            echo "--help              : Print help\n";
            echo "--directory=path    : Test path. The default is './'\n";
            echo "--recursive         : Test search will be recursive\n";
            echo "--parse-script=file : Path to the IPPcode22 parser file. The default is './parse.php'\n";
            echo "--int-script=file   : Path to the IPPcode22 interpret. The default is './interpret.py'\n";
            echo "--parse-only        : Run tests on the parser only. It can't be combined with the --int-script and --int-only options.\n";
            echo "--int-only          : Run tests on the interpret only. It can't be combined with the --parse-script, --parse-only options and --jexampath.\n";
            echo "  (If both parse-only and int-only parameters are not set, parser and interpreter tests will be run sequentially)\n";
            echo "--jexampath=path    : Path to the directory containing the jexamxml.jar file and a configuration file named options. The default is '/pub/courses/ipp/jexamxml/'\n";
            echo "--noclean           : Auxiliary files with interim results will not be deleted during test.php work\n\n";
            exit(0);
        } else {
            fwrite(STDERR, "10 - missing script parameter (if needed) or use of disabled parameter combination\n");
            exit(10);
        }
    }

    if (array_key_exists("directory",$args)) {
        $dir = $args["directory"];
    }

    if (!is_dir($dir)) {
        fwrite(STDERR, "41 - the specified directory or the specified file does not exist or is not accessible\n");
        exit(41);
    }

    if (array_key_exists("parse-script",$args)) {
        $parse_script = $args["parse-script"];
        if (!file_exists($parse_script)) {
            fwrite(STDERR, "41 - the specified directory or the specified file does not exist or is not accessible\n");
            exit(41);
        }
    }

    if (array_key_exists("int-script",$args)) {
        $int_script = $args["int-script"];
        if (!file_exists($int_script)) {
            fwrite(STDERR, "41 - the specified directory or the specified file does not exist or is not accessible\n");
            exit(41);
        }
    }

    if (array_key_exists("parse-only", $args)) {
        $parse_only = true;
    }

    if (array_key_exists("int-only", $args)) {
        $int_only = true;
    }

    if (array_key_exists("jexampath", $args)) {
        $jexampath = $args["jexampath"];
        if (!file_exists("$jexampath/jexamxml.jar")) {
            fwrite(STDERR, "41 - the specified directory or the specified file does not exist or is not accessible\n");
            exit(41);
        }
    }

    if (array_key_exists("recursive", $args)) {
        $recursive = true;
    }

    if (array_key_exists("noclean", $args)) {
        $noclean = true;
    }
    // Bad args sequence
    if (($parse_only and $int_only) or ($parse_only and array_key_exists("int-script", $args)) or ($int_only and array_key_exists("parse-script", $args)) or ($int_only and array_key_exists("jexampath", $args))) {
        fwrite(STDERR, "10 - missing script parameter (if needed) or use of disabled parameter combination\n");
        exit(10);
    }

    // Test search method
    if (!$recursive) {
        $src = new DirectoryIterator($dir);
    } else {
        $src = new RecursiveIteratorIterator(new RecursiveDirectoryIterator($dir), RecursiveIteratorIterator::SELF_FIRST);
    }

    $test_counter = 0;
    $passed_tests = 0;
    $failed_tests = 0;

    // Printing html out to stdout
    print_head();

    // Main loop
    foreach ($src as $src) {
        $out = "";
        if ($src->getExtension() == "src") {
            $src = $src->getPathname();
            $test_counter += 1;

            $src_path = realpath($src);

            $wout_extension = substr($src, 0, -4);

            $test_name = basename($src, ".src");
            $path = realpath($dir).realpath(substr($wout_extension, strlen($dir)));

            $ref_rc = $wout_extension.".rc";
            $ref_out = $wout_extension.".out";
            $in = $wout_extension.".in";

            $out_tmp = $wout_extension.".out_tmp";
            $xml_tmp = $wout_extension.".xml_tmp";
            $expected_retval = create_rc($ref_rc);
            create_out($ref_out);
            create_in($in);
            f_open($out_tmp);

            // Create unique tmp file for retvals
            $tmp_rc = tempnam($dir, "tmp_rc_");
            $tmp = fopen($tmp_rc, "w+");

            // First step of comparison, only retvals are compared with diff

            // parse-only test
            if ($parse_only) {
				exec("php8.1 \"$parse_script\" < \"$src_path\" > \"$out_tmp\"", $null, $exit_code);

                f_write($tmp, $exit_code);

                exec("diff -qZ \"$ref_rc\" \"$tmp_rc\"", $null, $diff_rc);

            } else // int-only test
            if ($int_only) {
                exec("python3.8 \"$int_script\" --source=\"$src_path\" < \"$in\" > \"$out_tmp\"", $output, $exit_code);

                f_write($tmp, $exit_code);

                exec("diff -qZ \"$ref_rc\" \"$tmp_rc\"", $null, $diff_rc);
            } else { // both parse and int test, if parser returns 0, interpet will be executed
                f_open($xml_tmp);

                exec("php8.1 \"$parse_script\" < \"$src_path\" > \"$xml_tmp\"", $null, $exit_code);
                if ($exit_code == 0) {
                    exec("python3.8 \"$int_script\" --source=\"$xml_tmp\" < \"$in\" > \"$out_tmp\"", $output, $exit_code);
                }

                f_write($tmp, $exit_code);

                exec("diff -qZ \"$ref_rc\" \"$tmp_rc\"", $null, $diff_rc);
                f_clean("$xml_tmp", $noclean);
            }
            f_clean($tmp_rc, $noclean);

            // In case of successful retvals comparison, program compare outputs. In parse-only tests with jexamxml, int and both with diff
            if ($diff_rc == 0) {
                if ($exit_code != 0) {
                    $passed_tests += 1;
                    // Test passed successfuly, parser or interpet returned expected retval
                    $out = "NaN";
                    $status = "OK";
                } else {
                    if ($parse_only) { // Ouput comparison in parse-only option
                        exec("java -jar \"$jexampath/jexamxml.jar\" \"$ref_out\" \"$out_tmp\"", $null, $diff_content);
                    } else { // Ouput comparison in int-only and both options
                        exec("diff -qZ \"$ref_out\" \"$out_tmp\"", $null, $diff_content);
                    }
                    if ($diff_content == 0) {
                        $passed_tests += 1;
                        // Test passed successfuly, parser or interpet returned 0 and outputs are identical
                        $out = "Identical";
                        $status = "OK";
                    } else {
                        $failed_tests += 1;
                        // Test failed, parser or interpet returned 0, but outputs are different
                        $out = "Different";
                        $status = "FAIL";
                    }
                }
            } else {
                $failed_tests += 1;
                // Test failed, parser or interpet did not return expected retval
                $out = "NaN";
                $status = "FAIL";
            }
            // Prin
            print_body($test_counter, $path, $test_name, $expected_retval, $exit_code, $out, $status);

            if(file_exists($ref_out.".log")) {
                f_clean($ref_out.".log", $noclean);
	        }
            f_clean($out_tmp, $noclean);
        }
    }

    // Printing html out to stdout
    print_summary($test_counter, $passed_tests, $failed_tests);
    print_end();

    // Function creates in file if it is missing
    function create_in($in) {
        if (!file_exists($in)) {
            $file = fopen($in, "w+");
            fwrite($file, "");
            fclose($file);
        }
    }

    // Function creates out file if it is missing
    function create_out($ref_out) {
        if (!file_exists($ref_out)) {
            $file = fopen($ref_out, "w+");
            fwrite($file, "");
            fclose($file);
        }
    }

    // Function creates rc file if it is missing and returns expected retval
    function create_rc($ref_rc) {
        if (!file_exists($ref_rc)) {
            $file = fopen($ref_rc, "w+");
            fwrite($file, "0");
            fclose($file);
            return 0;
        } else {
            $file = fopen($ref_rc, "r");
            $expected_retval = intval(fread($file, filesize($ref_rc)));
            fclose($file);
            return $expected_retval;
        }
    }

    // Function delete tmp file
    function f_clean($file, $noclean) {
        if (!$noclean) {
            unlink($file);
        }
    }

    // Function opens file with "w" rule
    function f_open($file) {
        $file_created = fopen($file, "w");
        fclose($file_created);
    }

    // Function writes data into file
    function f_write($file, $data) {
        fwrite($file, $data);
        fclose($file);
    }
?>
