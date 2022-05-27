## 2019_Historical_HCR_lists

Clarivate Analytics前身是著名信息服务提供商—汤森路透社（Thomson Reuters）的知识产权和科学分部，这个下载的榜单是Clarivate Analytics根据全世界科研工作者在过去几年内论文被引用的次数及影响力而选出近几千名学者(见https://recognition.webofscience.com/awards/highly-cited/2019/)。Clarivate Analytics评论到所有入选科学家“的研究成果在其研究领域内都是极具价值及影响力的”。汤姆森路透社是全球著名的学术方面的咨询机构。每年汤姆森路透社都会利用其研究解决方案Web of KnowledgeTM中的数据来分析和预测最有影响力的研究人员。 

这个list里面提供了各个领域的高被引用学者，我们选择的是最近的年份（2019年，文件：2019_HCR.xlsx），领域是Economics and Business的113位学者（但是只选择了112位，因为学者Peters, Glen P.的h-index不能导出有bug），和Comupter Science的107位学者。这些学者的信息（名字、机构）分别存在文件author_econ.csv和author_cs.csv中。

我们还收集了清华大学部分学者的信息。经管学院经济系：白重恩，陆毅，苏良军。（我们选择的是Scopus查询结果中h-index ≥ 20 的教授）；计算机系：？？？

因此，经济商业总共有115位学者，计算机总共有？？？位学者。

## Author_Econ_Detail / Author_CS_Detail
每个学者什么时间发表了什么文章，截至现在引用多少的信息

## author_econ.csv / author_cs.csv

First Name
Last Name
ID              在Scopus中的唯一ID，也是文件夹Author_Econ_Detail / Author_CS_Detail 的文件名
Documents       总共发表文章数量
Cited By        所有文章引用数之和
Preprints       当前（2022.5.28）preprints的数量
Coauthor        Coauthor的数量
Topics          研究涉及到的主题，【有缺失值是0】。
Awarded Grants  是否有某一种奖
Category        要么是Economics and Business，要么是Computer Science
Primary Affiliation 主要就职单位
Secondary Affiliations 第二就职单位


