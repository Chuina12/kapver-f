from django.contrib import admin
from . models import Candidature,CandidatureEntreprise,Offre,Candidat,UserModel,Entreprise,Employer,FicheEmployer,Fiche,Facture,Ficheentreprise,Heure_sup,Compteur,Signature,Facturier,Mesfactures,Masignature,GriseSalariale,Collaborateur,Dokumente,Conge,Demande_conges,Kapver_info,Banniere1,Banniere2

class AdminDokumente(admin.ModelAdmin):
    list_display = ('name','doc','date')

class AdminCandidature(admin.ModelAdmin):
    list_display = ('intitule','nom','message','cv')

class AdminCandidatureEntreprise(admin.ModelAdmin):
    list_display = ('entreprise','phone','domain','adresse','message','date')

class AdminOffre(admin.ModelAdmin):
    list_display = ('domain','titre','description','date','expiration')

class AdminCandidat(admin.ModelAdmin):
    list_display = ('offre','nom','message','cv','date')


class AdminUserModel(admin.ModelAdmin):
    list_display = ('username','travailleur','entreprise')


class AdminEntreprise(admin.ModelAdmin):
    list_display = ('gerant','nom_entreprise','date','adresse','email','BP')

class AdminEmployer(admin.ModelAdmin):
    list_display = ('nom','entreprise','date')

class AdminFicheEmployer(admin.ModelAdmin):
    list_display = ('employer','wochentag','datum','arbeitszeit1','arbeitszeit2','pause','stunden','valider')
class AdminFiche(admin.ModelAdmin):
    list_display = ('fiche','date','employer','valider','signer_entreprise','date','signer_employer','entreprise','date_signer_entreprise','date_signer_employer')

class AdminFicheentreprise(admin.ModelAdmin):
    list_display = ('employer','wochentag','datum','arbeitszeit','stunden','valider')

class AdminFacture(admin.ModelAdmin):
    list_display = ('client','date','facture')

class AdminHeure(admin.ModelAdmin):
    list_display = ('nh','employer','date')

class AdminCompteur(admin.ModelAdmin):
    list_display = ('cpt','date','employer')

class AdminSignature(admin.ModelAdmin):
    list_display = ('signature','entreprise','date','gerant')


class AdminFacturier(admin.ModelAdmin):
    list_display = ('bz','einheit','menge','date')


class AdminMesfactures(admin.ModelAdmin):
    list_display = ('user','mesfactures','date')

class AdminMasignature(admin.ModelAdmin):
    list_display = ('sig','employer','date')


class AdminGriseSalariale(admin.ModelAdmin):
    list_display = ('date','fichier')

class AdminCollaborateur(admin.ModelAdmin):
    list_display = ('nom','email','adresse','numero','code_pays')

class AdminDemande_conges(admin.ModelAdmin):
    list_display =('reponse','demande','employer','entreprise','date')

class CongeAdmin(admin.ModelAdmin):
    list_display = ('name','employer', 'geb', 'personalnummer', 'von', 'bis', 'resturlaub', 'diesesjahr', 'datum_antrag', 'unterschrift_arbeitnehmer', 'begrundung_arbeitgeber', 'unterschrift_arbeitgeber')


# A PROPOS DE L'INDEX.HTML
class Kapver_infoAdmin(admin.ModelAdmin):
    list_display = ('nom', 'image', 'specialisation', 'recrutement_international', 'critere')

# caroussel
class Banniere1Admin(admin.ModelAdmin):
    list_display = ('titre', 'image_caroussel1', 'description')

class Banniere2Admin(admin.ModelAdmin):
    list_display = ('titre', 'image_caroussel2', 'description1', 'description2')


admin.site.register(Collaborateur,AdminCollaborateur)
admin.site.register(GriseSalariale,AdminGriseSalariale)
admin.site.register(Masignature,AdminMasignature)
admin.site.register(Mesfactures,AdminMesfactures)
admin.site.register(Facturier,AdminFacturier)
admin.site.register(Signature,AdminSignature)
admin.site.register(Compteur,AdminCompteur)
admin.site.register(Heure_sup,AdminHeure)
admin.site.register(Ficheentreprise,AdminFicheentreprise)
admin.site.register(Facture,AdminFacture)
admin.site.register(Fiche,AdminFiche)
admin.site.register(FicheEmployer,AdminFicheEmployer)
admin.site.register(Employer,AdminEmployer)
admin.site.register(Entreprise,AdminEntreprise)
admin.site.register(Candidat,AdminCandidat)
admin.site.register(Offre,AdminOffre)
admin.site.register(Candidature,AdminCandidature)
admin.site.register(CandidatureEntreprise,AdminCandidatureEntreprise)
admin.site.register(UserModel,AdminUserModel)
admin.site.register(Dokumente,AdminDokumente)
admin.site.register(Conge, CongeAdmin)
admin.site.register(Demande_conges,AdminDemande_conges)
admin.site.register(Kapver_info, Kapver_infoAdmin)
admin.site.register(Banniere1, Banniere1Admin)
admin.site.register(Banniere2, Banniere2Admin)
