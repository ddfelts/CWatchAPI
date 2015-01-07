from reportlab.lib.enums import TA_LEFT, TA_RIGHT, TA_CENTER, TA_JUSTIFY
from reportlab.lib import colors
from reportlab.lib.pagesizes import letter, landscape
from reportlab.platypus import Paragraph, Spacer, Image, Frame,Table, TableStyle, NextPageTemplate, PageTemplate, BaseDocTemplate,LongTable,CondPageBreak
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.lib import utils
from reportlab.lib.colors import red, green, black, blue, lightblue, HexColor, lightgrey, grey
from reportlab.platypus.flowables import Flowable, PageBreak
from reportlab.lib.styles import ParagraphStyle as PS
from reportlab.platypus.tableofcontents import TableOfContents


class cwPDF:

      def __init__(self,doc):
          self.docname = doc
          self.page_counter = 2
          self.w,self.h = letter
          self.doc = BaseDocTemplate(self.docname,pagesize=letter)
          self.landscape = Frame(self.doc.leftMargin,
                                 self.doc.bottomMargin,
                                 self.doc.height,
                                 self.doc.width,
                                 id="Normal")

          self.portrait = Frame(self.doc.leftMargin,
                                self.doc.bottomMargin,
                                self.doc.width,
                                self.doc.height,
                                id="Normal")

          self.tportrait = Frame(self.doc.leftMargin,
                                self.doc.bottomMargin,
                                self.doc.width,
                                self.doc.height,
                                id="Normal")
          ttemplate = PageTemplate(id='tportrait',frames =self.tportrait, onPage=self.make_title_page)
          ptemplate = PageTemplate(id='portrait',frames =self.portrait, onPage=self.make_portrait)
          ltemplate = PageTemplate(id='landscape',frames =self.landscape, onPage=self.make_landscape)
          self.doc.addPageTemplates([ttemplate,ptemplate,ltemplate]) 
          self.styles = getSampleStyleSheet()
          
          self.start = ""
          self.end = ""
          self.story = []
          self.pgType = "Letter"
          self.image = ""
          self.cimage = ""
          self.client = ""


          self.toc = TableOfContents()
	  self.toc.levelStyles = [  
	            PS(fontName='Times-Bold', fontSize=10, name='TOCHeading1', leftIndent=20, firstLineIndent=-20, spaceBefore=10, leading=16),  
	            PS(fontSize=10, name='TOCHeading2', leftIndent=40, firstLineIndent=-20, spaceBefore=5, leading=12),  
	            ]  


      def addTOC(self, page):
	  self.toc.beforeBuild()
          self.story.insert(page, NextPageTemplate('portrait'))
	  self.story.insert(page+1, self.toc);
          self.story.insert(page+2, PageBreak())

      def setCImage(self,image):
          self.cimage = image

      def setPImage(self,image):
          self.image = image

      def setTitle(self,text):
          self.title = text

      def setClient(self,text):
          self.client = text

      def setDates(self,start,end):
          self.startDate = start
          self.endDate = end

      def setClient(self,text):
          self.client = text

      def make_portrait(self,canvas,doc):
          canvas.saveState()
          canvas.setPageSize(letter)
          canvas.setFont("Times-Roman",10)
          canvas.drawString(6.25 * inch, self.h - 25,"Client Name: %s " % (self.client))
          canvas.line(.50 * inch, self.h - 33, 8 * inch, self.h - 33)
          canvas.line(.50 * inch,.50 * inch, 8 * inch,.50 * inch)
          canvas.drawString(inch * 7.25, 0.25 * inch, "Page %d" % doc.page)
          canvas.drawString(inch * .50, 0.25 * inch, "Confidential Document.")
          canvas.restoreState()

      def make_landscape(self,canvas,doc):
          canvas.saveState()
          canvas.setFont("Times-Roman",10)
          canvas.setPageSize(landscape(letter))
          canvas.line(.50 * inch, self.w - 33, 10.75 * inch,self.w - 33)
          canvas.line(.50 * inch,.50 * inch, 10.75 * inch,.50 * inch)
          canvas.drawString(inch * 10.75, 0.75 * inch, "Page %d" % doc.page)
          canvas.drawString(inch * 1.75, 0.75 * inch, "Confidential Document.")
          canvas.drawString(9.50 * inch,self.w - 25 ,"Client: %s" % self.client)
          canvas.restoreState()

      def make_title_page(self,canvas,doc):
          canvas.saveState()
          canvas.setFont("Times-Bold",20)
          canvas.setFillColor(lightblue)
          canvas.drawString(1 * inch,9 * inch , self.title)
          canvas.setFont("Times-Bold",12)
          canvas.setFillColor(black)
          canvas.drawString(1 * inch,8.70 * inch,"Start (%s) - End (%s)" % (self.startDate,self.endDate))
          canvas.drawString(1 * inch,8.45 * inch,"Client: %s" % self.client)
          canvas.setFont("Times-Roman",10)
          canvas.setFillColor(grey)
          canvas.drawString(1 * inch,2.20 * inch,"Confidential: The following report contains confidential information. Do not distribute, email, mail, fax, or transfer ")
          canvas.drawString(1 * inch,2.05 * inch,"via any electronic mechanism unless it has been approved by the recipient company's security policy. All copies and")
          canvas.drawString(1 * inch,1.90 * inch,"backups of this document should be saved on protected storage at all times. Do not share any of the information")
          canvas.drawString(1 * inch,1.75 * inch,"contained within this report with anyone unless they are authorized to view the information. Violating within this ")
          canvas.drawString(1 * inch,1.60 * inch,"report with anyone unless they are authorized to view the information. Violating any of the previous instructions is")
          canvas.drawString(1 * inch,1.45 * inch,"grounds for termination.")
          if self.image != "":
                aspect = self.get_aspect(self.image)
                canvas.drawImage(self.image,self.w-150,self.h-80,width=120,height=(120 * aspect))
          if self.cimage != "":
                aspect = self.get_aspect(self.cimage)
                canvas.drawImage(self.cimage,2.0625 * inch,self.h-400,width=self.w/2,height=(self.w/2 * aspect))
          canvas.restoreState()

      def get_aspect(self,path):
          img = utils.ImageReader(path)
          iw,ih = img.getSize()
          aspect = ih / float(iw)
          return aspect

      def setPortrait(self):
          self.story.append(NextPageTemplate('portrait'))
          self.addPageBreak()

      def setLandscape(self):
          self.story.append(NextPageTemplate('landscape'))
          self.addPageBreak()

      def setDates(self,start,end):
          self.startDate = start
          self.endDate = end

      def setCanvas(self,canvas):
          self.canvas = canvas  

      def addStory(self,text):
          t = Paragraph(text,self.styles["Normal"])
          self.story.append(t)
          self.story.append(Spacer(1,12))       

      def addStoryTitle(self,text):
          t = Paragraph(text,self.styles["Heading1"])
          self.story.append(t)
          self.story.append(Spacer(1,8))
          self.toc.addEntry(1, text, self.page_counter)

      def getKeys(self,data):
             all = []
             for f in data.keys():
                 all.append(f)
             return all

      def addTable(self,ndata):
          data = []
          keys = self.getKeys(ndata)
          data.append(keys)
          for x in ndata:
              lister = []
              for b in keys:
                  outb = ndata[b]
                  t = Paragraph(str(outb),self.styles["Normal"])
                  lister.append(t)
          data.append(lister)

          tblStyle = TableStyle([('TEXTCOLOR',(0,0),(-1,-1),black),
                                 ('VALIGN',(0,0),(-1,-1),'TOP'),
                                 ('BOX',(0,0),(-1,-1),1,black),
                                 ('INNERGRID',(0,0),(-1,-1),1,black),
                                 ('BACKGROUND',(0,0),(-1,0),lightblue)])

          t = LongTable(data,repeatRows=1)
          t.setStyle(tblStyle)
          self.story.append(t)
          self.story.append(CondPageBreak(6))
 
      def addPageBreak(self):
          self.story.append(PageBreak())
          self.page_counter = self.page_counter + 1

      def addImage(self,image,w,h):
          self.story.append(Image(image,w,h))
          self.story.append(Spacer(1,12))

      def savePDF(self):
          self.addTOC(2)
          self.doc.build(self.story)
          self.story = []
