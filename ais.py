import asyncio
import json
from playwright.async_api import async_playwright

async def run_automation():
    async with async_playwright() as p:
        # เปลี่ยนเป็น headless=True เพื่อให้รันบน GitHub Actions ได้
        browser = await p.chromium.launch(headless=True)
        page = await browser.new_page()
        
        print("1. เข้าสู่ AIS PLAY...")
        await page.goto("https://app.ais-vidnt.com/portal/live", wait_until="networkidle")
        
        # --- ด่านที่ 1 ---
        await page.wait_for_selector("text=เข้าใช้งานแบบไม่ลงทะเบียน", timeout=20000)
        await page.click("text=เข้าใช้งานแบบไม่ลงทะเบียน")
        print("-> ผ่านด่าน 1")
        
        # --- ด่านที่ 2 ---
        ok_button = page.locator("button:has-text('ตกลง')")
        await ok_button.wait_for(state="visible", timeout=10000)
        await ok_button.click(force=True)
        print("-> ผ่านด่าน 2")
        await asyncio.sleep(3) # รอรายการช่องโหลด
        
        # --- ดึงข้อมูลเฉพาะช่อง 2 และ 3 ---
        targets = ["2", "3"]
        results = []
        
        for ch_num in targets:
            print(f"กำลังบันทึกช่อง {ch_num}...")
            await page.click(f"text={ch_num}", timeout=10000)
            await asyncio.sleep(3) # รอให้ URL อัปเดต
            
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
