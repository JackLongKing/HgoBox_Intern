# -*- coding: utf-8 -*-

# ============================================================================
# movies.xml
# =======================================================
# <collection shelf="New Arrivals">
# 	<movie title="Enemy Behind">
# 		<type>War, Thriller</type>
# 		<format>DVD</format>
# 		<year>2003</year>
# 		<rating>PG</rating>
# 		<stars>10</stars>
# 		<description>Talk about a US-Japan war</description>
# 	</movie>
# 	<movie title="Transformers">
# 		<type>Anime, Science Fiction</type>
# 		<format>DVD</format>
# 		<year>1989</year>
# 		<rating>R</rating>
# 		<stars>8</stars>
# 		<description>A schientific fiction</description>
# 	</movie>
# 	<movie title="Trigun">
# 		<type>Anime, Action</type>
# 		<format>DVD</format>
# 		<episodes>4</episodes>
# 		<rating>PG</rating>
# 		<stars>10</stars>
# 		<description>Vash the Stampede!</description>
# 	</movie>
# 	<movie title="Ishtar">
# 		<type>Comedy</type>
# 		<format>VHS</format>
# 		<rating>PG</rating>
# 		<stars>2</stars>
# 		<description>Viewable boredom</description>
# 	</movie>
# 	</collection>

# ============================================================================
# parse ==>using sax(simple API for xml)
# =======================================================
# python使用SAX解析xml
# SAX是一种基于事件驱动的API。利用SAX解析XML文档牵涉到两个部分:解析器和事件处理器。
# 解析器负责读取XML文档,并向事件处理器发送事件,如元素开始跟元素结束事件;而事件处理
# 器则负责对事件作出相应,对传递的XML数据进行处理。
#   1、对大型文件进行处理；
#   2、只需要文件的部分内容，或者只需从文件中得到特定信息。
#   3、想建立自己的对象模型的时候。
# 在python中使用sax方式处理xml要先引入xml.sax中的parse函数，还有xml.sax.handler中的ContentHandler。
#
# ContentHandler类方法介绍
# characters(content)方法
#
# 调用时机：
# 从行开始，遇到标签之前，存在字符，content的值为这些字符串。
# 从一个标签，遇到下一个标签之前， 存在字符，content的值为这些字符串。
# 从一个标签，遇到行结束符之前，存在字符，content的值为这些字符串。
# 标签可以是开始标签，也可以是结束标签。
#
# startDocument()方法
# 文档启动的时候调用。
#
# endDocument()方法
# 解析器到达文档结尾时调用。
#
# startElement(name, attrs)方法
# 遇到XML开始标签时调用，name是标签的名字，attrs是标签的属性值字典。
#
# endElement(name)方法
# 遇到XML结束标签时调用。
#
# make_parser方法
# 以下方法创建一个新的解析器对象并返回。
# xml.sax.make_parser( [parser_list] )
# 参数说明:
# parser_list - 可选参数，解析器列表
#
# parser方法
# 以下方法创建一个 SAX 解析器并解析xml文档：
# xml.sax.parse( xmlfile, contenthandler[, errorhandler])
# 参数说明:
# xmlfile - xml文件名
# contenthandler - 必须是一个ContentHandler的对象
# errorhandler - 如果指定该参数，errorhandler必须是一个SAX ErrorHandler对象
# parseString方法
# parseString方法创建一个XML解析器并解析xml字符串：
#
# xml.sax.parseString(xmlstring, contenthandler[, errorhandler])
# 参数说明:
# xmlstring - xml字符串
# contenthandler - 必须是一个ContentHandler的对象
# errorhandler - 如果指定该参数，errorhandler必须是一个SAX ErrorHandler对象
# =======================================================

# import xml.sax
#
# class MovieHandler(xml.sax.ContentHandler):
#     def __init__(self):
#         self.CurrentData=""
#         self.type=""
#         self.format=""
#         self.year=""
#         self.rating=""
#         self.stars=""
#         self.description=""
#
#     # 文档启动
#     def startDocument(self):
#         print("parsing xml file starts")
#
#     # 元素开始事件处理
#     def startElement(self,tag,attributes):
#         self.CurrentData=tag
#         if tag == "movie":
#             print("*****Movie*****")
#             title=attributes['title']
#             print("title: {0}".format(title))
#
#     # 元素结束事件处理
#     def endElement(self, tag):
#         if self.CurrentData=="type":
#             print("type: ",self.type)
#         elif self.CurrentData=="format":
#             print("format: ",self.format)
#         elif self.CurrentData=="year":
#             print("year: ",self.year)
#         elif self.CurrentData=="rating":
#             print("rating: ",self.rating)
#         elif self.CurrentData=="stars":
#             print("stars: ",self.stars)
#         elif self.CurrentData=="description":
#             print("description: ",self.description)
#         self.CurrentData=""
#
#     # 文档结束
#     def endDocument(self):
#         print("parsing xml file end!")
#
#     # 内容事件处理
#     def characters(self,content):
#         if self.CurrentData=="type":
#             self.type=content
#         elif self.CurrentData=="format":
#             self.format=content
#         elif self.CurrentData=="year":
#             self.year=content
#         elif self.CurrentData=="rating":
#             self.rating=content
#         elif self.CurrentData=="stars":
#             self.stars=content
#         elif self.CurrentData=="description":
#             self.description=content
#
# if __name__=="__main__":
#     # 创建一个xml Reader
#     parser=xml.sax.make_parser()
#     # 关闭命名空间
#     parser.setFeature(xml.sax.handler.feature_namespaces,0)
#     # 重写ContextHandler
#     Handler=MovieHandler()
#     parser.setContentHandler(Handler)
#     parser.parse("movies.xml")

# ============================================================================
# DOM
# =======================================================
# 使用xml.dom解析xml
# 文件对象模型（Document Object Model，简称DOM），是W3C组织推荐的处理可扩展置标语言的标准编程接口。
#
# 一个 DOM 的解析器在解析一个 XML 文档时，一次性读取整个文档，把文档中所有元素保存在内存中的一个树结构
# 里，之后你可以利用DOM 提供的不同的函数来读取或修改文档的内容和结构，也可以把修改过的内容写入xml文件。
# python中用xml.dom.minidom来解析xml文件，实例如下：
# =======================================================
# from xml.dom.minidom import parse
# import xml.dom.minidom
#
# DOMTree=xml.dom.minidom.parse("movies.xml")
# collection=DOMTree.documentElement
# if collection.hasAttribute("shelf"):
#     print("Root element: %s" % collection.getAttribute("shelf"))
#
# movies=collection.getElementsByTagName("movie")
#
# for movie in movies:
#     print("*****Movie*****")
#     if movie.hasAttribute("title"):
#         print("title: %s" % movie.getAttribute("title"))
#
#     type=movie.getElementsByTagName('type')[0]
#     print("type: %s" % type.childNodes[0].data)
#     format=movie.getElementsByTagName('format')[0]
#     print("format: %s" % format.childNodes[0].data)
#     rating=movie.getElementsByTagName("rating")[0]
#     print("rating: %s" % rating.childNodes[0].data)
#     description=movie.getElementsByTagName("description")[0]
#     print("description: %s" % description.childNodes[0].data)

# ============================================================================
# test.xml
# =======================================================
# <annotation>
# 	<folder>youlemei20180309</folder>
# 	<filename>img00001.jpg</filename>
# 	<path>F:\imageLabel\20180309\youlemei20180309\img00001.jpg</path>
# 	<source>
# 		<database>Unknown</database>
# 	</source>
# 	<size>
# 		<width>1280</width>
# 		<height>960</height>
# 		<depth>3</depth>
# 	</size>
# 	<segmented>0</segmented>
# 	<object>
# 		<name>youlemei</name>
# 		<pose>Unspecified</pose>
# 		<truncated>0</truncated>
# 		<difficult>0</difficult>
# 		<bndbox>
# 			<xmin>14</xmin>
# 			<ymin>144</ymin>
# 			<xmax>80</xmax>
# 			<ymax>239</ymax>
# 		</bndbox>
# 	</object>
# 	<object>
# 		<name>youlemei</name>
# 		<pose>Unspecified</pose>
# 		<truncated>0</truncated>
# 		<difficult>0</difficult>
# 		<bndbox>
# 			<xmin>72</xmin>
# 			<ymin>13</ymin>
# 			<xmax>337</xmax>
# 			<ymax>171</ymax>
# 		</bndbox>
# 	</object>
# </annotation>

# ============================================================================
# practice for pascal_voc xml format
# =======================================================
# from xml.dom.minidom import parse
# import xml.dom.minidom
#
# DOMTree=xml.dom.minidom.parse("test.xml")
# anno=DOMTree.documentElement
#
# folder=anno.getElementsByTagName("folder")[0]
# print("folder: %s" % folder.childNodes[0].data)
#
# filename=anno.getElementsByTagName("filename")[0]
# print("filename: %s" % filename.childNodes[0].data)
#
# path=anno.getElementsByTagName("path")[0]
# print("path: %s " % path.childNodes[0].data)
#
# sources=anno.getElementsByTagName("source")
# for source in sources:
#     print("===source===")
#     database=source.getElementsByTagName("database")[0]
#     print("database: %s" % database.childNodes[0].data)
#
# sizes=anno.getElementsByTagName("size")
# for size in sizes:
#     print("===sizes===")
#     width=size.getElementsByTagName("width")[0]
#     print("width: %s" % width.childNodes[0].data)
#     height=size.getElementsByTagName("height")[0]
#     print("height: %s" % height.childNodes[0].data)
#     depth=size.getElementsByTagName("depth")[0]
#     print("depth: %s" % depth.childNodes[0].data)
#
# segmented=anno.getElementsByTagName("segmented")[0]
# print("segmented: %s" % segmented.childNodes[0].data)
#
# objects=anno.getElementsByTagName("object")
# for object in objects:
#     print("===objects===")
#     name=object.getElementsByTagName("name")[0]
#     print("name: %s" % name.childNodes[0].data)
#     pose=object.getElementsByTagName("pose")[0]
#     print("pose: %s" % pose.childNodes[0].data)
#     truncated=object.getElementsByTagName("truncated")[0]
#     print("truncated: %s" % truncated.childNodes[0].data)
#     difficult=object.getElementsByTagName("difficult")[0]
#     print("difficult: %s" % difficult.childNodes[0].data)
#     bndboxes=object.getElementsByTagName("bndbox")
#     for bndbox in bndboxes:
#         print("===bndboxes===")
#         xmin=bndbox.getElementsByTagName("xmin")[0]
#         print("xmin: %s" % xmin.childNodes[0].data)
#         ymin=bndbox.getElementsByTagName("ymin")[0]
#         print("ymin: %s" % ymin.childNodes[0].data)
#         xmax=bndbox.getElementsByTagName("xmax")[0]
#         print("xmax: %s" % xmax.childNodes[0].data)
#         ymax=bndbox.getElementsByTagName("ymax")[0]
#         print("ymax: %s" % ymax.childNodes[0].data)

# ============================================================================
# Element Tree
# =======================================================
# XML文件格式介绍：
# <tag attrib = > text </tag> tail
# 例：<APP_KEY channel = 'CSDN'> hello123456789 </APP_KEY>
#
# tag，即标签，用于标识该元素表示哪种数据，即APP_KEY
# attrib，即属性，用Dictionary形式保存，即{'channel' = 'CSDN'}
# text，文本字符串，可以用来存储一些数据，即hello123456789
# tail，尾字符串，并不是必须的，例子中没有包含。
# ElementTree解析XML文件的过程：
# 导入ElementTree，import xml.etree.ElementTree as ET
# 解析Xml文件找到根节点：
# 直接解析XML文件并获得根节点，tree = ET.parse('country_data.xml') root = tree.getroot()
# 解析字符串，root = ET.fromstring(country_data_as_string)
# 遍历根节点可以获得子节点，然后就可以根据需求拿到需要的字段了。

# =======================================================
# ET_test.xml
# =======================================================
# <?xml version="1.0"?>
# <data>
#     <country name="Liechtenstein">
#         <rank>1</rank>
#         <year>2008</year>
#         <gdppc>141100</gdppc>
#         <neighbor name="Austria" direction="E"/>
#         <neighbor name="Switzerland" direction="W"/>
#     </country>
#     <country name="Singapore">
#         <rank>4</rank>
#         <year>2011</year>
#         <gdppc>59900</gdppc>
#         <neighbor name="Malaysia" direction="N"/>
#     </country>
#     <country name="Panama">
#         <rank>68</rank>
#         <year>2011</year>
#         <gdppc>13600</gdppc>
#         <neighbor name="Costa Rica" direction="W"/>
#         <neighbor name="Colombia" direction="E"/>
#     </country>
# </data>
# =======================================================
# import xml.etree.ElementTree as ET
#
# tree=ET.parse("ET_test.xml")
# root=tree.getroot()
# print("root-tag: ",root.tag,",root-attrib: ",root.attrib,",root-text: ",root.text)
# for child in root:
#     print("    child-tag: ",child.tag,",child-attrib: ",child.attrib,",child-text: ",child.text)
#     for sub in child:
#         print("        sub-tag: ",sub.tag,",sub-attrib: ",sub.attrib,",sub-text: ",sub.text)

# =======================================================
# 查找指定的子节点：
# 当XML文件较大或者其中的子节点tag非常多的时候，一个一个获取是比较麻烦的而且有很多不是我们需要的，这样我们可以通过find('nodeName')或者findall('nodeName')方法来查找指定tag的节点。
#
# find('nodeName')：表示在该节点下，查找其中第一个tag为nodeName的节点。
# findall('nodeName')：表示在该节点下，查找其中所有tag为nodeName的节点。
# =======================================================
# import xml.etree.ElementTree as ET
#
# tree=ET.parse("ET_test.xml")
# root=tree.getroot()
# aniNode=root.find('country')
# print("aniNode-tag: ",aniNode.tag,"aniNode-attrib: ",aniNode.attrib,"aniNode-text: ",aniNode.text)

# 删除指定的节点以及保存
# 在合并Manifest文件的时候，可能有一些重复的权限，那么怎么删除掉呢，删除指定节点可以通过
# remove(node)方法,移除指定的节点。
# 代码示例，比如我们想移除attribute中name为Liechtenstein的节点：

# =======================================================
import xml.etree.ElementTree as ET

tree=ET.parse("ET_test.xml")
root=tree.getroot()
aniNode=root.find("country")
if aniNode.attrib["name"] == "Liechtenstein":
    root.remove(aniNode)
tree.write("after_ET_test.xml")

# ============================================================================






