# Hastalik Teshis Sistemi
Yapay Zeka dersi grup projesi kapsamında geliştirilmiş, belirti tabanlı tıbbi teşhis sistemi.

Ne Yapar?
Belirtilerini seçiyorsun, sistem üç farklı yapay zeka tekniğini birleştirerek en olası hastalıkları sıralıyor.

Kullanılan Yapay Zeka Teknikleri
Mantık — Birinci Dereceden Mantık kuralları + Modus Ponens çıkarım motoru (24 kural, 18 hastalık)
Matematik — Bayes olasılığı, belirti-hastalık matrisi (18×29), kosinüs benzerliği, özdeğer analizi
Optimizasyon — Hill Climbing algoritması ile belirti ağırlıkları otomatik optimize ediliyor
Nasıl Çalıştırılır?
pip install flask numpy
python3 app.py
Tarayıcıda aç: http://localhost:5050

Bilgi Tabanı
18 hastalık
29 belirti
Tüm belirti-hastalık olasılıkları tıbbi literatüre dayalı
Teknolojiler
Python · Flask · NumPy · HTML/CSS/JavaScript
