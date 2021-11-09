class Parser {
    constructor($root) {
        this.root = $root;
        this.target_block_names = [
            'definition',
            'theorem',
            'registration',
            'scheme',
            'notation',
        ];
        this.target_CSS_selector = 'span.kw';
    }
    list_comments(article) {
        let comments = [];
        let counter = {}
        this.target_block_names.forEach(function (value) {
            counter[value] = 0;
        });
        for (let target of this.root.find(this.target_CSS_selector)) {
            //sometimes $(target).text() return string like "theorem " so trim()
            let block_name = $(target).text().trim();
            if (this.target_block_names.includes(block_name)) {
                let comment = new Comment(
                    article,
                    $(target),
                    block_name,
                    ++counter[block_name],
                    "comments"
                );
                comments.push(comment);
            }
        };
        return comments
    }
}
