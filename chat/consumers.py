
from channels.generic.websocket import AsyncWebsocketConsumer
import json
from channels.db import database_sync_to_async
from .models import *

class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        my_id = self.scope['user'].id
        other_user_id = self.scope['url_route']['kwargs']['id']
        if int(my_id) > int(other_user_id):
            self.room_name = f"{my_id}-{other_user_id}"
        else:
            self.room_name = f"{other_user_id}-{my_id}"
        
        self.room_group_name = 'chat_%s' % self.room_name

        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name,
        )
        await self.accept()
        

    # async def receive(self, text_data=None, bytes_data=None):
    #     data = json.loads(text_data)
    #     message = data['message']
    #     username = data['username']

    #     await self.save_message(username,self.room_group_name, message)
    #     await self.channel_layer.group_send(
    #         self.room_group_name, 
    #         {
    #             'type' : 'chat_msg',
    #             'message':message,
    #             'username':username,
    #         }
    #         )
    
    # async def chat_msg(self,event):
    #     message = event['message']
    #     username = event['username']

    #     await self.send(text_data=json.dumps({
    #         'message':message,
    #         'username':username
    #     }))

    async def receive(self, text_data=None, bytes_data=None):
        data = json.loads(text_data)
        message = data['message']
        username = data['username']

        await self.save_message(username, self.room_group_name, message)


        await self.channel_layer.group_send(
            self.room_group_name,
            {
                'type': 'chat_msg',
                'message': message,
                'username': username,
            }
        )

    async def chat_msg(self, event):
        message = event['message']
        username = event['username']

        await self.send(text_data=json.dumps({
            'message': message,
            'username': username,
        }))

    async def disconnect(self, code):
        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
        )

    @database_sync_to_async
    def save_message(self, username, thread_name, message):
        chat_obj = ChatMessage.objects.create(source=username, msg=message, thread=thread_name)
        other_user_id = self.scope['url_route']['kwargs']['id']
        get_user = User.objects.get(id=other_user_id)
    



       
class OnlineStatusConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        # my_id = self.scope['user'].id
        # other_user_id = self.scope['url_route']['kwargs']['id']
        
        # if int(my_id) > int(other_user_id):
        #     self.room_name = f"{my_id}-{other_user_id}"
        # else:
        #     self.room_name = f"{other_user_id}-{my_id}"
        
        # self.room_group_name = 'chat_%s' % self.room_name

        self.room_group_name = 'user'
        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name
        )

        await self.accept()

    async def receive(self, text_data=None, bytes_data=None):
        data = json.loads(text_data)
        username = data['username']
        connection_type = data['type']
        print(connection_type)
        await self.change_online_status(username, connection_type)

    async def send_onlineStatus(self, event):
        data = json.loads(event.get('value'))
        username = data['username']
        online_status = data['status']
        await self.send(text_data=json.dumps({
            'username':username,
            'online_status':online_status
        }))


    async def disconnect(self, message):
        self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
        )

    @database_sync_to_async
    def change_online_status(self, username, c_type):
        userprofile = Profile.objects.get(username=username)
        if c_type == 'open':
            userprofile.status = True
            userprofile.save()
        else:
            userprofile.status = False
            userprofile.save()
