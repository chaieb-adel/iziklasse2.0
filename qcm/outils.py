from .models import Niveau,Matiere

def get_niveau():
    return Niveau.objects.all()