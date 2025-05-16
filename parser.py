# -*- coding: utf-8 -*-
from telethon import TelegramClient
from database.models import Gift
from database.db import SessionLocal, init_db
from config import API_ID, API_HASH, SESSION_NAME
import re

init_db()
client = TelegramClient(SESSION_NAME, API_ID, API_HASH)

async def parse_gifts():
    try:
        with open("gift_urls.txt", encoding='utf-8-sig') as f:
            for line in f:
                if not line.strip():
                    continue
                    
                gift_type, max_id = line.strip().split()
                max_id = int(max_id)
                
                for gift_id in range(1, max_id + 1):
                    url = f"https://t.me/nft/{gift_type}-{gift_id}"
                    try:
                        entity = await client.get_entity(url)
                        if not entity.text: 
                            continue
                        
                        # ������� ����������
                        backdrop = re.search(r"backdrop:\s*(\w+)", entity.text, re.IGNORECASE)
                        model = re.search(r"model:\s*(\w+)", entity.text, re.IGNORECASE)
                        
                        # ���������� � ��
                        session = SessionLocal()
                        gift = Gift(
                            gift_id=gift_id,
                            gift_type=gift_type,
                            backdrop=backdrop.group(1) if backdrop else None,
                            model=model.group(1) if model else None,
                            url=url
                        )
                        session.add(gift)
                        session.commit()
                        print(f"�������: {url}")
                        
                    except Exception as e:
                        if "STARGIFT_SLUG_INVALID" in str(e):
                            break
                        print(f"������ {url}: {e}")
    
    except UnicodeDecodeError:
        print("������ ���������! ������������� gift_urls.txt � UTF-8")
    except Exception as e:
        print(f"����������� ������: {e}")

async def main():
    await client.start()
    await parse_gifts()
    await client.disconnect()

if __name__ == '__main__':
    client.loop.run_until_complete(main())