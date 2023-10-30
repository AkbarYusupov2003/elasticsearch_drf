from elasticsearch_dsl import analyzer, tokenizer


edge_ngram_analyzer = analyzer(
    'autocomplete_filter',
    tokenizer=tokenizer('trigram', 'ngram', min_gram=1, max_gram=2), # 'edge_ngram'
    filter=['lowercase'],
    #char_filter=["html_strip"]
)



# autocomplete": {
#     "type":      "custom",
#     "tokenizer": "standard",
#     "filter": [
#         "lowercase",
#         "autocomplete_filter" 
#     ]
# }



# "analyzer": {
# "analyzer_startswith": {
#         "tokenizer": "keyword",
#         "filter": "lowercase"
#     }
# }
# prefix_analyzer = analyzer(
#     "analyzer_startswith",
#     tokenizer=tokenizer("keyword"),
#     filter=["lowercase"]
# )
