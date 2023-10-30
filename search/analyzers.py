from elasticsearch_dsl import analyzer, tokenizer


edge_ngram_analyzer = analyzer(
    'autocomplete_filter',
    tokenizer=tokenizer('trigram', 'ngram', min_gram=1, max_gram=2), # 'edge_ngram'
    filter=['lowercase'],
)
