class TheoremSearcher:
    def search(self, query_text):
        
        search_results=[]
        
        '''
        {
            'label': 
            'text':
            'relevance':
            'filename':
            'line_no':
        }
        '''

        if(query_text=='theorem set c= set implies Cl ( set /\ set ) c= Cl ( set /\ set )'):
            search_results=[{'label': 'CLASSES1:68', 'text': 'the_transitive-closure_of (X /\ Y) c= the_transitive-closure_of X /\ the_transitive-closure_of Y;', 'relevance': 0.99, 'filename': 'classes1.abs', 'line_no': 322, },
                            {'label': 'FUNCT_4:6', 'text': 'for a,b being object holds\nX <> {} & X --> a c= Y --> b implies a = b;', 'relevance': 0.98, 'filename': 'funct_4.abs', 'line_no': 40, }]

        # URLを生成
        for search_result in search_results:
            url = 'http://mizar.org/version/current/html/' + search_result['label'].split(':')[0].lower() + '.html#t' + search_result['label'].split(':')[1]
            urldict = {'url': url}
            search_result.update(urldict)
        
        return search_results