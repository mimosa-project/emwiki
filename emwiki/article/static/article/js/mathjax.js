/* eslint-disable max-len */
MathJax = {
  tex2jax: {
    inlineMath: [['$', '$'], ['\\(', '\\)']],
    processEscapes: true,
  },
  tex: {
    packages: {'[+]': ['textmacros']},
    inlineMath: [ // start/end delimiter pairs for in-line math
      ['$', '$'],
      ['\\(', '\\)'],
    ],
    displayMath: [ // start/end delimiter pairs for display math
      ['$$', '$$'],
      ['\\[', '\\]'],
    ],
    processEscapes: true, // use \$ to produce a literal dollar sign
    processEnvironments: true, // process \begin{xxx}...\end{xxx} outside math mode
    processRefs: true, // process \ref{...} outside of math mode
    digits: /^(?:[0-9]+(?:\{,\}[0-9]{3})*(?:\.[0-9]*)?|\.[0-9]+)/,
    // pattern for recognizing numbers
    tags: 'none', // or 'ams' or 'all'
    tagSide: 'right', // side for \tag macros
    tagIndent: '0.8em', // amount to indent tags
    useLabelIds: true, // use label name rather than tag for ids
    multlineWidth: '85%', // width of multline environment
    maxMacros: 1000, // maximum number of macro substitutions per expression
    maxBuffer: 5 * 1024, // maximum size for the internal TeX string (5K)
    baseURL: // URL for use with links to tags (when there is a <base> tag in effect)
         (document.getElementsByTagName('base').length === 0) ?
          '' : String(document.location).replace(/#.*$/, ''),
  },
  options: {
    skipHtmlTags: [ //  HTML tags that won't be searched for math
      'script', 'noscript', 'style', 'textarea', 'pre',
      'code', 'annotation', 'annotation-xml',
    ],
    includeHtmlTags: { //  HTML tags that can appear within math
      'br': '\n', 'wbr': '', '#comment': '',
    },
    ignoreHtmlClass: 'no-mathjax', //  class that marks tags not to search
    processHtmlClass: 'mathjax', //  class that marks tags that should be searched
    compileError: function(doc, math, err) {
      doc.compileError(math, err);
    },
    typesetError: function(doc, math, err) {
      doc.typesetError(math, err);
    },
  },
};
