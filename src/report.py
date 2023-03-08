from src.classes.Validator_lxml import Validator
from src.types import *

# Syntax report stub
def report_syntax_v1(name, format, source, data) -> Evaluation:
    evaluation = Evaluation(
        aspect="syntax",
        is_valid=True,
        num_rules_fired=0,
        num_rules_failed=0,
        num_violations=0,
        violations=[]
    )
    return evaluation

# Peppol report stub
def report_peppol_v1(name, format, source, data) -> Evaluation:
    evaluation = Evaluation(
        aspect="peppol",
        is_valid=True,
        num_rules_fired=0,
        num_rules_failed=0,
        num_violations=0,
        violations=[]
    )
    return evaluation

# Syntax report stub
def report_wellformedness_v1(invoice: Invoice) -> Evaluation:
    evaluation = Evaluation(
        aspect="wellformedness",
        is_valid=True,
        num_rules_fired=0,
        num_rules_failed=1,
        num_violations=1,
        violations=[]
    )
    # model of evaluation with one violation
    # evaluation = Evaluation(
    #     aspect="wellformedness",
    #     is_valid=True,
    #     num_rules_fired=0,
    #     num_rules_failed=1,
    #     num_violations=1,
    #     violations=[Violation(
    #         rule_id="wellformedness",
    #         is_fatal=True,
    #         location=LocationLine(
    #             line=1,
    #             column=1
    #         ),
    #         test="test",
    #         message="message",
    #         suggestion="suggestion"
    #     )]
    # )
    return evaluation

# Peppol report stub
def report_schemavalid_v1(invoice: Invoice) -> Evaluation:
    evaluation = Evaluation(
        aspect="schema",
        is_valid=True,
        num_rules_fired=0,
        num_rules_failed=0,
        num_violations=0,
        violations=[]
    )
    validator = Validator("src/validation_artefacts/UBL-Invoice-2.1.xsd")

    # The directory with XML files
    file_path = "test/example_files/AUInvoice_valid.xml"

    if validator.validate(file_path):
        print('Valid! :)')
    else:
        evaluation.is_valid = False
        print('Not valid! :(')
    return evaluation