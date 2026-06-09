import asyncio
import websockets

async def chat():
    user_id = input("أدخل اسم المستخدم الخاص بك: ")
    uri = f"ws://localhost:8000/ws/{user_id}"
    
    async with websockets.connect(uri) as websocket:
        print("تم الاتصال بنجاح!")
        
        # مهمة لاستقبال الرسائل في الخلفية
        async def receive():
            while True:
                message = await websocket.recv()
                print(f"\n{message}")
        
        # مهمة لإرسال الرسائل
        async def send():
            while True:
                msg = input("أنت: ")
                await websocket.send(msg)

        await asyncio.gather(receive(), send())

asyncio.run(chat())
