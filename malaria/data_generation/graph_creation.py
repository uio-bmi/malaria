import subprocess
import logging

def run_command(command, return_raw=False):
    logging.debug("Running command: " + command)
    res = subprocess.check_output(command.split())
    if res == "" or return_raw:
        return res
    return res.decode("utf-8")


def run_mafft(in_file_name, out_file_name, gap_extension_penalty=-0.7, limit_to_n_first_sequences=None):

    if limit_to_n_first_sequences is not None:
        logging.info(" Limiting mafft to only use the first %d sequences to create msa" % limit_to_n_first_sequences)
        with open(in_file_name + "_limited.tmp", "w") as limited_file:
            with open(in_file_name) as in_file:
                n = 0
                for line in in_file:
                    limited_file.writelines([line])
                    n += 1
                    if n >= limit_to_n_first_sequences * 2:  # Assuming dual-line fasta
                        break

        in_file_name = in_file_name + "_limited.tmp"

    command = "mafft --thread 80 --ep %.2f --auto --reorder %s" \
                % (gap_extension_penalty, in_file_name)
    with open(out_file_name, "w") as outfile:
        subprocess.call(command.split(), stdout=outfile)

    logging.info("Wrote mafft results to %s" % out_file_name)



