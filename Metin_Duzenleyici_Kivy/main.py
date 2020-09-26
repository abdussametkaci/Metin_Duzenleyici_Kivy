import os, sys
from kivy.uix.label import Label
from kivy.app import App
from kivy.uix.popup import Popup
from kivy.config import Config

class FarkliKaydetForm(Popup):
    pass

class DosyaAcForm(Popup):
    pass

class DosyaKaydedilmediForm(Popup):
    pass

class YeniDosyaForm(Popup):
    pass

class CikmadanOnceForm(Popup):
    pass

class MetinDuzenleyici(App):
    def on_start(self):
        Config.set("kivy", "exit_on_escape", "False")#geri tuşuna basarak çıkmayı engelledik
    
    def farkliKaydetDialog(self):
        form = FarkliKaydetForm()
        form.open()

    def farkliKaydetSecim(self, form):
        secilen_dosya = form.ids.dosya_secim.selection
        if secilen_dosya:
            if len(secilen_dosya) > 0:
                dosyaAdi = os.path.split(secilen_dosya[0])[1]
                form.ids.dosya_adi.text = dosyaAdi

    def farkliKaydetIslevi(self, form):
        self.son_patika = form.ids.dosya_secim.path
        self.son_dosya = form.ids.dosya_adi.text
        self.dosyaKaydet()

    def dosyaKaydet(self):
        if not self.son_dosya:
            self.hataGöster("Dosya adı verdiğinizden emin misiniz?")
        else:
            try:
                dosya_tam_isim = os.path.join(self,son_patika, self.son_dosya)
                f = open(dosya_tam_isim+"~", "w")
                f.write(self.root.ids.metin.text)
                f.close()
                os.rename(dosya_tam_isim+"~", dosya_tam_isim)
            except:
                self.hataGöster("Dosyayı yazamadım. Nedeni: [color=#FF0000]%s[/color]"%str(sys.exc_info()[1]))
        self.metin_değişti = False
        self.root.ids.cik_dugmesi.background_color = [1, 0, 0, 1]

    def hataGöster(self, hata):
        içerik = Label(text = hata, markup = True)
        popup = Popup(title = "Yapamadım!", content = içerik)
        popup.size_hint = (0.7, 0.7)
        içerik.bind(on_touch_down = popup.dismiss)
        popup.open()

    def dosyaKaydetIslevi(self):
        if self.son_dosya:
            self.dosyaKaydet()
        else:
            self.farkliKaydetDialog()

    def metinDeğişti(self, nesne, değer):
        if self.ilkAçılış:
            self.ilkAçılış = False
        else:
            self.metin_değişti = True
            self.root.ids.cik_dugmesi.background_color = [1, 0, 0, 1]

    def dosyaAcIsleviDialog(self):
        if self.metin_değişti:
            kaydedilmedi_form = DosyaKaydedilmediForm()
            kaydedilmedi_form.open()
        else:
            self.dosyaAcDialog()

    def dosyaAcDialog(self):
        form = DosyaAcForm()
        form.open()

    def dosyaOku(self, dosya_secim):
        if dosya_secim.selection:
            if len(dosya_secim.selection) > 0:
                (self.son_patika, self.son_dosya) = os.path.split(dosya_secim.selection[0])
                try:
                    self.root.ids.metin.text = open(dosya_secim.selection[0]).read()
                    self.root.ids.metin.cursor = self.root.ids.metin.get_cursor_from_index(0)
                    self.metin_değişti = False
                    self.root.ids.cik_dugmesi.background_color = [1, 0, 0, 1]
                except:
                    self.hataGöster("Dosyayı okuyamadım. Nedeni: [color=#FF0000]%s[/color]"%str(sys.exc_info()[1]))
            else:
                self.hataGöster("Dosya seçtiğinizden emin misiniz?")

    def dosyaKaydedilmediKaydet(self, kok):
        if self.son_dosya:
            self.dosyaKaydet()
            kok.dismiss()
            self.dosyaAcDialog()
        else:
            kok.dismiss()
            self.hataGöster("Dosya adı yok. Farklı kaydedin lütfen")
            
    def yeniDosyaAcIslevi(self):
         if self.metin_değişti:
             form = YeniDosyaForm()
             form.open()
         else:
             self.yeniDosyaAc()

    def yeniDosyaAc(self):
        self.root.ids.metin.text = ""
        self.son_dosya = ""
        self.root.ids.cik_dugmesi.background_color = [0, 1, 0, 1]

    def cik(self):
        if self.metin_değişti:
            kaydedilmedi_form = CikmadanOnceForm()
            kaydedilmedi_form.open()
        else:
            self.stop()
    
    def build(self):
        self.son_patika = os.getcwd()
        self.son_dosya = ""
        self.metin_değişti = False
        self.root.ids.cik_dugmesi.background_color = [1, 0, 0, 1]
        self.root.ids.metin.bind(text = self.metinDeğişti)
        self.ilkAçılış = True
MetinDuzenleyici().run()
