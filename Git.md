PS D:\Github\PlantSimulation> git --version
git version 2.54.0.windows.1

เริ่มต้นโปรเจกต์ (Setup)

1. git init : สร้าง Repository ใหม่ในเครื่อง

git clone URL_PROJECT : คัดลอกโปรเจกต์จาก GitHub ลงเครื่อง

git config --global user.name "Your Name" : ตั้งชื่อผู้ใช้งาน

git config --global user.email "email@example.com" : ตั้งอีเมล

2. วงจรการทำงานปกติ (Daily Workflow)
   git status : ตรวจสอบสถานะไฟล์ (มีอะไรแก้ไขบ้าง)

git add . : เลือกไฟล์ทั้งหมดเตรียมบันทึก (Stage)

git commit -m "Your Message" : บันทึกการเปลี่ยนแปลงพร้อมคำอธิบาย

git push origin BRANCH_NAME : ส่ง Code จากเครื่องขึ้นไปบน GitHub

3. การอัปเดตงาน (Syncing)
   git fetch : ตรวจสอบการอัปเดตจาก Server

git pull : ดึงข้อมูลล่าสุดลงมาที่เครื่องทันที

4. การจัดการ Branch (Branching)
   git branch : ดูรายชื่อ Branch ทั้งหมด

git checkout -b BRANCH_NAME : สร้าง Branch ใหม่และสลับไปใช้งานทันที

git checkout BRANCH_NAME : สลับไป Branch ที่ต้องการ

git merge BRANCH_NAME : รวม Code จาก Branch อื่นเข้ากับ Branch ปัจจุบัน

5. คำสั่งเสริมอื่นๆ
   git log : ดูประวัติการ Commit ย้อนหลัง

git remote -v : ดูว่าเครื่องเราเชื่อมกับ GitHub URL ไหนอยู่

git reset --hard : ยกเลิกการแก้ไขทั้งหมดและย้อนกลับไปจุดล่าสุด


[www.youtube.com/watch?v=seAxzKm9yhw](https://www.youtube.com/watch?v=seAxzKm9yhw)
