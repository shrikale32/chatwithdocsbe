import json
import openai

from rest_framework import generics, status, parsers, renderers
from rest_framework.views import APIView
from rest_framework.decorators import api_view, renderer_classes
from rest_framework.response import Response
from rest_framework.renderers import JSONRenderer

from django.http import StreamingHttpResponse
from django.core.files.storage import default_storage

from file_upload_chat.api.serializers import ChatSerializer, MessageSerializer
from file_upload_chat.models import Chat, Messages
from file_upload_chat.utils import split_docs, embed_documents, get_pinecone_index, get_context

from langchain.document_loaders import S3FileLoader

openai_model = "gpt-3.5-turbo"
max_responses = 1
temperature = 0.7
max_tokens = 512

class ChatList(generics.ListCreateAPIView):
    queryset = Chat.objects.all()
    parser_classes = (parsers.FormParser, parsers.MultiPartParser, parsers.FileUploadParser)
    serializer_class = ChatSerializer
    # permission_classes = [IsAuthenticated, IsOwner] 


class ChatDetail(generics.RetrieveDestroyAPIView):
    queryset = Chat.objects.all()
    serializer_class = ChatSerializer
    # throttle_classes = [DocumentDeleteThrottle]
    # permission_classes = [IsAuthenticated, IsOwner]
    
    def get_queryset(self, request):
        return Chat.objects.filter(userId=request.GET.get('userId'))
    
    def perform_destroy(self, instance):

        s3_key = instance.file.name
        print(s3_key)

        if s3_key:
            try:
                default_storage.delete(s3_key)
                instance.delete()
                return Response(status=status.HTTP_204_NO_CONTENT)
            except Exception as e:
                return Response({"error": f"Error deleting file: {str(e)}"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        else:
            return Response({"error": "File not found"}, status=status.HTTP_404_NOT_FOUND)


class LoadDataPineCone(APIView):
    def post(self, request):
        chat_id=request.data.get('chat_id')
        chat = Chat.objects.filter(id=chat_id).first()
        
        if chat:
            file_key = chat.file.name
            print("File_key", file_key)
        
        if file_key:
            loader = S3FileLoader("projectbinder", str(file_key))
            document = loader.load()
            split_documents = split_docs(document)
            embeddings = embed_documents(split_documents, str(file_key))
            index = get_pinecone_index()
            index.upsert(vectors=embeddings)
            
        return Response({'response': 'Success'})


class MessageDetail(generics.RetrieveAPIView):
    serializer_class = MessageSerializer

    def post(self, request):
        chatId = request.data.get('chatId')
        messages = Messages.objects.filter(chatId=chatId)
        serializer = MessageSerializer(messages, many=True)
        
        return Response(serializer.data, status=status.HTTP_200_OK)
 
     
@api_view(['POST'])
@renderer_classes([JSONRenderer])
def chat_view(request):
        data = json.loads(request.body)
        messages = data.get('messages')
        chatId = data.get('chatId')
        
        chat = Chat.objects.filter(id=chatId).first()
        
        if chat:
            file_key = chat.file.name
        
        if not chat:
            return Response({'error': 'Chat not found'}, status=status.HTTP_404_NOT_FOUND)
        
        if messages:
                lastMessage = messages[-1]
                print(lastMessage['content'])
                
        context = get_context(lastMessage['content'], str(file_key))
        
        prompt = {
            "role": "system",
            "content": f"""AI assistant is a brand new, powerful, human-like artificial intelligence.
            The traits of AI include expert knowledge, helpfulness, cleverness, and articulateness.
            AI is a well-behaved and well-mannered individual.
            AI is always friendly, kind, and inspiring, and he is eager to provide vivid and thoughtful responses to the user.
            AI has the sum of all knowledge in their brain and is able to accurately answer nearly any question about any topic in conversation.
            START CONTEXT BLOCK
            {context}
            END OF CONTEXT BLOCK
            AI assistant will take into account any CONTEXT BLOCK that is provided in a conversation.
            If the context does not provide the answer to the question, the AI assistant will say, "I'm sorry, but I don't know the answer to that question."
            AI assistant will not apologize for previous responses but instead will indicate new information was gained.
            AI assistant will not invent anything that is not drawn directly from the context."""
        }

        try:
            response = openai.ChatCompletion.create(
                model=openai_model,
                temperature=temperature,
                max_tokens=max_tokens,
                n=max_responses,
                top_p=1,
                frequency_penalty=0,
                presence_penalty=0,
                messages=[
                    prompt,
                    {"role": "user", "content": lastMessage['content'] }
                ],
                stream=True,
            )
            
            def generate_stream(response):
                for chunk in response:
                    current_content = chunk["choices"][0]["delta"].get("content", "")
                    yield current_content

            return StreamingHttpResponse(generate_stream(response), content_type="text/event-stream")

        except Exception as e:
            print("Error in creating campaigns from openAI:", str(e))
            raise Response({'error': 'Chat not found'}, status=status.HTTP_503_SERVICE_UNAVAILABLE)
            
  
"""Alternative approach to query OpenAI API using langchain"""
# class ChatLLMResponse(generics.RetrieveAPIView):
#     queryset = Chat.objects.all()
#     serializer_class = ChatSerializer
    
#     def get(self, request, pk):
#         try:
#             instance = self.get_object()
#             s3_key = instance.file.name
#         except Chat.DoesNotExist:
#             return Response({'error': 'Chat not found'}, status=status.HTTP_404_NOT_FOUND)
        
#         if s3_key:
#             query = request.GET.get('query')
#             loader = S3FileLoader("projectbinder", s3_key)
#             documents = loader.load()
#             chain = load_qa_chain(llm=OpenAI(), chain_type="map_reduce")
#             response = chain.run(input_documents=documents, question=query)
#             print(response)
#             return Response({'response' :response}, status=status.HTTP_200_OK)
            
        
    
    