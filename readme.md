# Early Detection of Promising Companies for Venture Capital Financing Using Patent Data

## Bachelor's Project - Fall 2019

This study investigates the potential of using public patent data for early detection of promising companies for venture capital financing. We aimed to search for patents based on their technology fields or usage scope, independent of classification and keyword appearance. We used a bag-of-words representation of patent abstracts and t-SNE visualization to identify patent clusters, testing the method with two case studies. Our goal is to create an interactive tool demonstrating the value of this approach in a venture capital context by examining prominent patent holders and distribution in specific technology subfields.

### Introduction

Venture capital financing supports early-stage companies with high growth potential. Using machine learning and data mining, existing patent data could help investors identify companies investing in or researching specific technologies. Patents are of interest to investors as they indicate the owner's engagement with the patented technology, signaling intent to develop or produce a product.

### Methodology

1. **Data Source**: We used PatentsView's bulk data on granted patents for this study due to its accessibility and manageable size. We focused on abstracts and bibliographical information, as these are most relevant for searching and refining search results. Recent patents or patent applications are particularly interesting in the venture capital context.
2. **Data Preprocessing**: We preprocess data by stemming words, removing stop words, and filtering low-occurrence words to eliminate irrelevant information. This helps create a more efficient comparison between patents, reducing memory and runtime requirements.
3. **Bag-of-words**: We transform abstracts into an NxM matrix, where each row represents a patent and each column a unique word. We use cosine similarity to compare patent vectors. To account for varying word relevance, we employ term frequency-inverse document frequency (tf-idf) values, resulting in an NxM matrix A.
4. **Similarity matrix**: We create an NxN matrix B, where values B_ij represent cosine similarity between patent i and j. This pairwise similarity matrix is based on the input NxM matrix A from the previous step.
5. **Visualization**: We use t-SNE for visualizing high-dimensional data, focusing on demonstrating the data's potential usefulness for venture capital. The t-SNE algorithm conserves distance between points, emphasizing similarity in content for exploring and searching patents in this vector space.
6. **Scalability**: The total number of unique words in our vocabulary is a function of the number of patents included in our analysis. We limit memory to 4GB, allowing for approximately 22,360 patents for storage, with subsets no larger than N=2,000 in the application due to computational limitations.

![Figure 1](https://github.com/sverrirhd/patent-visualization-with-t-SNE/raw/main/images/figure1.png)

*Figure 1: The relationship between the number of unique words and the number of abstracts in a collection is approximated for 1 to 12,000 patents. The similarity matrix becomes the limiting factor after 5,000 patents. With a 4GB memory limit, we can store up to 22,360 patents.*

### Results

We examine two case studies to test the approach: one showing dissimilar abstracts forming separate clusters, and another demonstrating similar abstracts forming overlapping clusters.

1. **Separation between dissimilar clusters**: We combine three subsets of patents containing the words 'drugs', 'footwear', and 'speech'. We examine cases where words appear in the abstract and title. The sizes of subsets with these words in abstracts are 831, 552, and 1409, and in titles are 217, 364, and 571, respectively. To avoid selection bias, we apply our method with and without search terms in the abstracts. In Figure 2, dots represent patents, and colors indicate the subset each patent is from.

![Figure 2](https://github.com/sverrirhd/patent-visualization-with-t-SNE/raw/main/images/figure2.png)
Figure 2: First case study (Dissimilar subsets). Clear clustering with negligible overlap is observed. Locality in the vector space is tied to similarity in abstract content. The presence of search terms in the title or abstract doesn't significantly affect the results.

Overlapping of similar clusters: The second case study uses phrases 'drugs', 'surgery', and 'physiological', expecting overlapping clusters due to similar medical and biological terminology.

![Figure 3](https://github.com/sverrirhd/patent-visualization-with-t-SNE/raw/main/images/figure3.png)
Figure 3: Second case study (similar subsets). More overlap is seen when search terms appear in the abstract, while less overlap occurs when search terms are in the title. This indicates greater specialization when a term is in the title.

Conclusion
This paper aimed to show that patent abstracts can be used to find similar patents. We transformed abstracts into a BoW vector space and used t-SNE for visualization. Two case studies demonstrated that similar patents form clusters together and similar clusters overlap more than dissimilar ones. This suggests that a useful tool for venture capitalists to search for patents and explore domains without relying on simple word searches or patent categories is possible.

Repository Contents
This GitHub repository includes all the notebooks and images used in the report:

Notebooks: Jupyter notebooks containing the code for data preprocessing, analysis, and visualization.
Images: images and visualizations used in the report.
Please refer to the notebooks and images to further explore the methodology and results of this study.

## Appendix

### Demonstration of practical application

Once we saw it was possible to cluster patents in this way, we tried to implement these methods in a simple interactive tool that can demonstrate the usefulness of this method on a real-life example. The example used here is the intention to investigate the distribution of patents in the subfield of ‘network patents specifically relating to social networks.

First, the user searches for all patents, with and after the year 2018, containing the word network in the abstract. The tool finds 32,814 such patents. The tool automatically reduces the size to 10,000 before the next step by random selection to reduce computation time and memory required.

![Figure 4: User interface for patent space visualization tool](https://github.com/sverrirhd/patent-visualization-with-t-SNE/raw/main/images/figure4.png)

The user then goes to the next tab, specifies some keywords for labeling the patents. The user picks the words ‘neural’, ‘wireless’, and ‘social’, since the user wants to see how much these subdomains overlap. The user finds that these subsets separate themselves quite a bit in the ‘network’ domain. The user then hovers over some points in dense clusters, attempting to find other ‘network’ subdomains.

![Figure 5: User interface for patent space visualization tool with the results of the search and patents colored based on if they contain a certain term or not](https://github.com/sverrirhd/patent-visualization-with-t-SNE/raw/main/images/figure5.png)

The user finds the words ‘communication’, ‘packet’, and ‘virtual’ to be common in some clusters and adds these terms to be labeled. This gives a much more detailed picture of subdomains and their relation to social networks.

![Figure 6: User interface for patent space visualization tool with the results of the search and patents colored based on if they contain a certain term or not, with more colors and more terms that show the clustering of patents with certain terms](https://github.com/sverrirhd/patent-visualization-with-t-SNE/raw/main/images/figure6.png)

The user then finally drags a shape around the most prominent clusters of patents labeled with the ‘social’ search term and then goes to the next tab.

![Figure 7: User interface for patent space visualization tool with the results of the search and patents colored based on if they contain a certain term or not, with more colors and more terms that show the clustering of patents with certain terms. Here we also see highlighted, a region with patents containing the words "social"](https://github.com/sverrirhd/patent-visualization-with-t-SNE/raw/main/images/figure7.png)

There, the user is able to see the most prominent patent holders in this domain. To no surprise, the biggest number of patents in the selected area belongs to Facebook, then followed by IBM and Google.

![Figure 8: The second part of the UI with a timeline of the highlighted patents from the previous image and a breakdown of which companies own these patents.](https://github.com/sverrirhd/patent-visualization-with-t-SNE/raw/main/images/figure8.png)
The user is interested in seeing how the acquisition of patents by Facebook has developed and if there is some trend that can give insight. The user double-clicks on Facebook's label in the legend and is presented with a similar graph where Facebook's patent history has been isolated.
