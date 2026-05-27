import asyncio
import json
from playwright.async_api import async_playwright

async def run_automation():
    async with async_playwright() as p:
        # กำหนดขนาดหน้าจอให้เสถียร
        browser = await p.chromium.launch(headless=True)
        context = await browser.new_context(
            viewport={"width": 1280, "height": 720},
            user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
        )
        page = await context.new_page()
        
        print("1. เข้าสู่ AIS PLAY...")
        # แก้ไขตรงนี้: ใช้ wait_until="commit" (แค่เริ่มส่งข้อมูลก็ไปต่อเลย ไม่ต้องรอโหลดเสร็จทั้งหมด)
        await page.goto("https://app.ais-vidnt.com/portal/live", wait_until="commit", timeout=60000)
        
        # --- ด่านที่ 1 ---
        print("กำลังรอปุ่ม ด่านที่ 1...")
        # ขยายเวลาการรอปุ่มเพิ่มเผื่อเน็ตฝั่งนอกโหลดหน้าเว็บช้า
        await page.wait_for_selector("text=เข้าใช้งานแบบไม่ลงทะเบียน", timeout=40000)
        await page.click("text=เข้าใช้งานแบบไม่ลงทะเบียน")
        print("-> ผ่านด่าน 1")
        
        # --- ด่านที่ 2 ---
        ok_button = page.locator("button:has-text('ตกลง')")
        await ok_button.wait_for(state="visible", timeout=20000)
        await ok_button.click(force=True)
        print("-> ผ่านด่าน 2")
        await asyncio.sleep(5) # ขยายเวลารอรายการช่องโหลดนิดนึง
        
        # --- ดึงข้อมูลเฉพาะช่อง 2 และ 3 ---
        targets = ["2", "3"]
        results = []
        
        for ch_num in targets:
            print(f"กำลังบันทึกช่อง {ch_num}...")
            await page.click(f"text={ch_num}", timeout=15000)
            await asyncio.sleep(4) # รอให้ URL อัปเดต
            
            # บันทึก URL
            current_url = page.url
            results.append({"channel": ch_num, "url": current_url})
            print(f"บันทึกสำเร็จ: {current_url}")
            
        with open("test_channels.json", "w", encoding="utf-8") as f:
            json.dump(results, f, ensure_ascii=False, indent=4)
            
        print("--- บันทึกช่อง 2 และ 3 ลง test_channels.json เรียบร้อย ---")
        await browser.close()

if __name__ == "__main__":
    asyncio.run(run_automation())
            results.append({"channel": ch_num, "url": current_url})
            print(f"บันทึกสำเร็จ: {current_url}")
            
        with open("test_channels.json", "w", encoding="utf-8") as f:
            json.dump(results, f, ensure_ascii=False, indent=4)
            
        print("--- บันทึกช่อง 2 และ 3 ลง test_channels.json เรียบร้อย ---")
        await browser.close()

if __name__ == "__main__":
    asyncio.run(run_automation())
