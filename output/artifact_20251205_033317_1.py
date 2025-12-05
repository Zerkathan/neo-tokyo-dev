import json
from typing import List, Dict, Any
import asyncio
from tenacity import retry, stop_after_attempt, wait_fixed
import aiohttp
import sqlite3

class Target:
    def __init__(self, name: str, url: str, selector: str, change_type: str, threshold: float = None):
        self.name = name
        self.url = url
        self.selector = selector
        self.change_type = change_type
        self.threshold = threshold

class ChangeDetector:
    def __init__(self, targets: List[Target]):
        self.targets = targets
        self.db_path = 'changes.db'

    async def fetch_data(self, session: aiohttp.ClientSession, target: Target) -> str:
        try:
            async with session.get(target.url) as response:
                return await response.text()
        except aiohttp.ClientError as e:
            print(f"Failed to fetch data for {target.name}: {e}")
            return None

    def parse_data(self, html: str, selector: str) -> Any:
        soup = BeautifulSoup(html, 'html.parser')
        element = soup.select_one(selector)
        if element:
            return element.get_text(strip=True)
        return None

    @retry(stop=stop_after_attempt(3), wait=wait_fixed(2))
    async def detect_changes(self):
        async with aiohttp.ClientSession() as session:
            for target in self.targets:
                html = await self.fetch_data(session, target)
                if html is not None:
                    current_value = self.parse_data(html, target.selector)

                    conn = sqlite3.connect(self.db_path)
                    cursor = conn.cursor()
                    cursor.execute('SELECT * FROM changes WHERE target_name=? ORDER BY timestamp DESC LIMIT 1', (target.name,))
                    last_record = cursor.fetchone()

                    if last_record:
                        old_value = last_record[3]
                        if self.check_change(old_value, current_value, target.change_type, target.threshold):
                            await self.notify(target, old_value, current_value)
                            cursor.execute('UPDATE changes SET notified=1 WHERE id=?', (last_record[0],))
                    else:
                        cursor.execute('INSERT INTO changes (target_name, timestamp, old_value, new_value, notified) VALUES (?, ?, ?, ?, 0)', (target.name, datetime.now(), None, current_value, False))

                    conn.commit()
                    conn.close()

    def check_change(self, old_value: Any, new_value: Any, change_type: str, threshold: float = None) -> bool:
        if change_type == 'price_drop':
            try:
                old_price = float(old_value.replace(',', '.'))
                new_price = float(new_value.replace(',', '.'))
                return new_price < old_price
            except ValueError:
                return False
        elif change_type == 'content_change':
            return old_value != new_value
        return False

    async def notify(self, target: Target, old_value: Any, new_value: Any):
        if target.chat_id:
            await self.send_telegram_message(target.chat_id, f'Change detected in {target.name}: {old_value} -> {new_value}')
        if target.webhook_url:
            await self.send_discord_webhook(target.webhook_url, f'Change detected in {target.name}: {old_value} -> {new_value}')

    async def send_telegram_message(self, chat_id: str, message: str):
        # Implementar envío de mensaje a Telegram
        pass

    async def send_discord_webhook(self, webhook_url: str, message: str):
        # Implementar envío de webhook a Discord
        pass

class Notifier:
    def __init__(self, targets: List[Target]):
        self.targets = targets

    async def notify_changes(self):
        detector = ChangeDetector(self.targets)
        await detector.detect_changes()

async def add_target(targets: List[Target], new_target: Target) -> None:
    targets.append(new_target)

async def list_targets(targets: List[Target]) -> None:
    for target in targets:
        print(f'Name: {target.name}, URL: {target.url}, Selector: {target.selector}, Change Type: {target.change_type}')

async def run_detector(detector: ChangeDetector) -> None:
    while True:
        await detector.detect_changes()
        await asyncio.sleep(target.check_interval)

async def test_target(targets: List[Target], target_name: str) -> None:
    for target in targets:
        if target.name == target_name:
            detector = ChangeDetector([target])
            await detector.detect_changes()
            break

async def clean_and_optimize_db():
    conn = sqlite3.connect('changes.db')
    cursor = conn.cursor()
    cursor.execute('VACUUM')
    conn.commit()
    conn.close()

if __name__ == '__main__':
    with open('targets.json', 'r') as file:
        config = json.load(file)
        targets = [Target(**t) for t in config['targets']]

    notifier = Notifier(targets)

    # Ejemplo de uso
    asyncio.run(run_detector(notifier))