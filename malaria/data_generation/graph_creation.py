import subprocess
import logging

def run_command(command, return_raw=False):
    logging.debug("Running command: " + command)
    res = subprocess.check_output(command.split())
    if res == "" or return_raw:
        return res
    return res.decode("utf-8")


def run_mafft(in_file_name, out_file_name, gap_extension_penalty=-0.7):
    command = "mafft --thread 80 --ep %.2f --auto --reorder %s" \
                % (gap_extension_penalty, in_file_name)
    with open(out_file_name, "w") as outfile:
        subprocess.call(command.split(), stdout=outfile)

    logging.info("Wrote mafft results to %s" % out_file_name)



