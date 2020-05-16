from Bio.Alphabet import IUPAC
from Bio.Seq import Seq
from Bio.Blast import NCBIWWW
from Bio.Blast import NCBIXML


def check_sequence(seq):
    seq = seq.upper().strip()
    warning = ""
    if len(seq) % 3 != 0:
        warning = "Warning: sequence is not a multiple of three"
    if seq == "":
        return "", "", "", "", ""
    elif seq.strip("ATGCN") == "":
        bio_sequence = Seq(seq, IUPAC.ambiguous_dna)
        rna_sequence = bio_sequence.transcribe()  # assuming that given sequence is coding sequence
        protein_sequence = bio_sequence.translate()  # also assuming thas given sequence is coding sequence
        print(rna_sequence)
        print(protein_sequence)
        return "DNA sequence", seq, rna_sequence, protein_sequence, warning
    elif seq.strip("AUGCN") == "":
        return "RNA sequence", seq, "", "", ""
    elif seq.strip("AKLSYWGQDMNTRIPHFCVE") == "":
        return "Protein sequence", seq, "", "", ""
    else:
        return "neither a DNA sequence, RNA sequence nor a Protein sequence", seq, "", "", ""


def automatic_blast(seq):
    print("BLASTing... This may take a while")
    result_handle = NCBIWWW.qblast("blastp", "nr", seq, format_type="XML", hitlist_size=10)
    print("BLASTing finished. Preparing accession codes.")
    return result_handle


def xml_parser(result_handle):
    blast_record = NCBIXML.read(result_handle)
    acc_code_list = []
    for alignment in blast_record.alignments:
        for hsp in alignment.hsps:
            alignment_title = alignment.title
            acc_code = alignment_title.split("|", 2)[1]
            acc_code_list.append(acc_code)
    return acc_code_list

