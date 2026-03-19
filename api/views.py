from rest_framework.decorators import api_view
from rest_framework.response import Response

@api_view(['GET'])
def test_spojeni(request):
    # Tento slovník se automaticky převede na formát JSON
    data = {
        "status": "success",
        "message": "Ahoj! Backend a frontend spolu úspěšně komunikují."
    }
    return Response(data)