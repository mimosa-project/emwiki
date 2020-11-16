class TheoremSearcher:
    def Searcher(query_text):
        
        search_results=[]
        
        if(query_text=='theorem set c= set implies Cl ( set /\ set ) c= Cl ( set /\ set )'):
            search_results=[{'Label': 'CLASSES1:68', 'Text': 'the_transitive-closure_of (X /\ Y) c= the_transitive-closure_of X /\ the_transitive-closure_of Y;', 'Relevance': 0.99, 'File': 'classes1.abs 322'},
                            {'Label': 'FUNCT_4:6', 'Text': 'for a,b being object holds\nX <> {} & X --> a c= Y --> b implies a = b;', 'Relevance': 0.98, 'File': 'funct_4.abs 40'}]

        # URLを生成
        for search_result in search_results:
            url = 'http://mizar.org/version/current/html/' + search_result['Label'].split(':')[0].lower() + '.html#t' + search_result['Label'].split(':')[1]
            urldict = {'URL': url}
            search_result.update(urldict)
        
        return search_results

        search_result['Label'].split(':')[0]