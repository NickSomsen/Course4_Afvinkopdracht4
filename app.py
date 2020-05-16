from flask import Flask, render_template, request
from functions import check_sequence, automatic_blast, xml_parser

app = Flask(__name__)


@app.route('/')
def sequence_checker():
    sequence = request.args.get("sequence", "")
    sequence_type, sequence, rna_seq, protein_seq, warning = check_sequence(sequence)
    if sequence_type == "Protein sequence":
        result_handle = automatic_blast(sequence)
        acc_code_list = xml_parser(result_handle)
    else:
        acc_code_list = ""
    return render_template("base.html", sequence_type=sequence_type, sequence=sequence, rna_sequence=rna_seq, protein_sequence=protein_seq, warning=warning, acc_code_list=acc_code_list)


if __name__ == '__main__':
    app.run()
