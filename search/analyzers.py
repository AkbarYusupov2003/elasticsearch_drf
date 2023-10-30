from elasticsearch_dsl import analyzer, tokenizer


edge_ngram_analyzer = analyzer(
    'autocomplete_filter',
    tokenizer=tokenizer('trigram', 'ngram', min_gram=3, max_gram=4), # 'edge_ngram'
    filter=['lowercase'],
)
