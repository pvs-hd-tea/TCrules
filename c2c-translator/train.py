import parser

if __name__ == "__main__":

    print("Creating RuleSet...")
    rule_set = parser.RuleSet()
    
    print("Deriving rules using the parallel corpus...")
    rule_set.derive_rules(parser.files)
    
    print("Storing rules...")
    rule_set.save_rules()
    rule_set.save_keywords()
