from elasticsearch_dsl import analyzer, tokenizer


multiple_words_analyzer = analyzer(
    'multiple_words_analyzer',
    tokenizer=tokenizer('multiple_words_analyzer_ngram_analyzer', 'ngram', min_gram=10, max_gram=11),
    filter=['lowercase', "stop", "shingle", "snowball",] 
)

# edge_ngram
strict_edge_ngram_analyzer = analyzer(
    'strict_edge_ngram_analyzer',
    tokenizer=tokenizer('strict_edge_ngram_analyzer_tokenizer', 'edge_ngram', min_gram=7, max_gram=8),
    filter=['lowercase', "stop", "shingle", "snowball",] 
)

medium_edge_ngram_analyzer = analyzer(
    'medium_edge_ngram_analyzer',
    tokenizer=tokenizer('medium_edge_ngram_analyzer_tokenizer', 'edge_ngram', min_gram=6, max_gram=7),
    filter=['lowercase', "stop", "shingle", "snowball" ]
)

soft_edge_ngram_analyzer = analyzer(
    'soft_edge_ngram_analyzer',
    tokenizer=tokenizer('soft_edge_ngram_analyzer_tokenizer', 'edge_ngram', min_gram=4, max_gram=5, token_chars=["letter","digit"]),
    filter=['lowercase', "stop", "shingle", "snowball"]
)

very_soft_edge_ngram_analyzer = analyzer(
    'very_soft_edge_analyzer',
    tokenizer=tokenizer('very_soft_edge_ngram_tokenizer', 'edge_ngram', min_gram=3, max_gram=4),
    filter=['lowercase', "stop", "shingle", "snowball"]
)

# ngram
strict_ngram_analyzer = analyzer(
    'strict_ngram_analyzer',
    tokenizer=tokenizer('strict_ngram_analyzer_tokenizer', 'ngram', min_gram=7, max_gram=8),
    filter=['lowercase', "stop", "shingle", "snowball"]
)

medium_ngram_analyzer = analyzer(
    'medium_ngram_analyzer',
    tokenizer=tokenizer('medium_ngram_analyzer_tokenizer', 'ngram', min_gram=6, max_gram=7),
    filter=['lowercase', "stop", "shingle", "snowball"]
)

# person

soft_ngram_analyzer = analyzer(
    'soft_ngram_analyzer',
    tokenizer=tokenizer('soft_ngram_analyzer_tokenizer', 'ngram', min_gram=3, max_gram=4),
    filter=['lowercase', "stop", "shingle", "snowball"]
)