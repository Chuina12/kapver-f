from django.shortcuts import render,redirect
from .models import Candidature,CandidatureEntreprise,Offre,Candidat,Entreprise,FicheEmployer,UserModel,Employer,Fiche,Ficheentreprise,Heure_sup,Compteur,Signature,Facturier,Mesfactures,Masignature,GriseSalariale,Collaborateur,Dokumente,Conge,Demande_conges,Kapver_info,Banniere1,Banniere2
from django.contrib import messages
from django.shortcuts import get_object_or_404
from django.conf import settings
from django.core.mail import send_mail, EmailMessage
from datetime import datetime, timedelta,time
from django.db.models import Sum
from fpdf import FPDF
from django.core.files import File
from send_mail import SendMail
from django.conf import settings
from django.http import HttpResponse
from django.core import mail
from django.template.loader import render_to_string
from django.utils.html import strip_tags
# from django.utils.translation import activate
import os
import logging
from django.template import TemplateDoesNotExist
from .tasks import envoyer_candidature_email
from django.urls import reverse


def index(request):
    query=Offre.objects.all()
    kapver_info = Kapver_info.objects.all()
    for info in kapver_info:
        info.critere_list = info.critere.split(',')
    banniere1 = Banniere1.objects.all()
    banniere2 = Banniere2.objects.all()
    try:
        return render(request, 'index.html', {'query':query, 'kapver_info':kapver_info, 'banniere1':banniere1, 'banniere2':banniere2})
    except TemplateDoesNotExist as e:
        return HttpResponse(f"Template not found: {str(e)}", status=500)


def employeur(request):
    if request.method=='POST':
        phone = request.POST.get('phone')
        entreprise = request.POST.get('entreprise')
        domain = request.POST.get('domain')
        adresse_email = request.POST.get('adresse_email')
        adresse = request.POST.get('adresse')
        message = request.POST.get('message')
        data = CandidatureEntreprise.objects.create(phone=phone,entreprise=entreprise,adresse_email=adresse_email,domain=domain,adresse=adresse,message=message)
        messages.success(request,'Merci pour votre demande,Nous vous contacterons !')
        return redirect('employeur')
    return render(request,'pages/employeur.html')


def candidature(request):
    if request.method=='POST':
        intitule = request.POST.get('intitule')
        nom = request.POST.get('nom')
        message = request.POST.get('message')
        cv = request.FILES.get('cv')
        print('eded',intitule)
        cand = Candidature.objects.create(intitule=intitule,nom=nom,message=message,cv=cv)
        cand.save()
        messages.success(request,'votre candidature a ete soumis avec succes !')
        return redirect('candidature')
    else:
        pass
    return render(request,'pages/candidature.html')

"""
def contact(request):
    if request.method == 'POST':
        subject = request.POST.get('subject')
        message = request.POST.get('message')
        from_email = request.POST.get('email')
	dest = settings.EMAIL_HOST_USER
        recipient_list = [dest]  # Mettez ici votre adresse email

        try:
            # Log the email being sent
            logger.info(f'Sending contact form email from: {from_email} to: {recipient_list}')

            send_mail(subject, message, from_email, recipient_list)
            messages.success(request, 'Message envoyé avec succès')
        except Exception as e:
            messages.error(request, f'Erreur lors de l\'envoi du message : {e}')

    return render(request, 'pages/contact.html')

"""
def offres(request):
    query =Offre.objects.all()
    return render(request,'pages/offres.html',{'query':query})

def conditions(request):
    return render(request,'pages/conditions.html')

def details(request, pk):
    obj = get_object_or_404(Offre, pk=pk)
    if request.method == 'POST':
        offr = obj.titre
        nom = request.POST.get('nom')
        message = request.POST.get('message')
        cv = request.FILES.get('cv')

        if nom and message and cv:
            # Créer une instance du candidat
            datas = Candidat.objects.create(nom=nom, message=message, cv=cv, offre=obj)
            datas.save()
            # Envoyer l'e-mail de candidature de manière asynchrone
            envoyer_candidature_email.delay(nom, message, datas.cv.path, obj.titre)

            messages.success(request, 'Candidature envoyée avec succès.')
            return redirect(reverse('details', kwargs={'pk':pk}))
        else:
            messages.error(request, 'Tous les champs sont requis.')
    return render(request, 'pages/details.html', {'obj': obj})

def candidature_email(request, pk):
    offre = get_object_or_404(Offre, pk=pk)
    candidat = get_object_or_404(Candidat)
    return render(request, 'pages/candidature_email.html', {'offre':offre, 'candidat':candidat})


#views for admin spaces
def dashboard(request):
    if request.user.is_authenticated:
        if request.user.membre_staff == True:
            number_candidature = Candidature.objects.all().count()
            number_recrut = CandidatureEntreprise.objects.all().count()
            entrep = Entreprise.objects.all()
            usere = request.user
            # employer = Employer.objects.get(nom=usere)[0]
            # nb = FicheEmployer.objects.filter(employer=employer,valider=True).count()
            emp = Employer.objects.all()
            entreprise = Entreprise.objects.select_related('gerant').filter(gerant=request.user)
            # print('efefefrfrfgrgr',entreprise)

            if request.method =="POST":
                entr = request.POST.get('entreprise')
                obj = Entreprise.objects.get(nom_entreprise=entr)
                entre = obj.nom_entreprise
                verify_exist = Signature.objects.filter(entreprise=obj)
                if len(verify_exist) ==0:
                    signature = request.FILES.get('signature')
                    user_o = request.user
                    gerant = UserModel.objects.get(username=user_o)
                    infos = Signature.objects.create(gerant=gerant,signature=signature,entreprise=obj)
                    infos.save()
                    messages.success(request,'signature enregistrer avec success !')
                    return redirect('dashboard')
                else:
                    messages.success(request,'signature existente !')
                    return redirect('dashboard')
                print('dsdfdfvedv',verify_exist)

                # datas = Signature.objects
            verify=''
            verify2=''
            if request.user.entreprise == True:
                try:
                    me = request.user
                    obj_user = Entreprise.objects.get(gerant=me)
                    verify = Fiche.objects.filter(entreprise = obj_user,valider=True,signer_entreprise=True).count()
                    verify2 = Fiche.objects.filter(entreprise = obj_user,valider=True,signer_entreprise=False).count()
                    print('efefefefefefef',verify)
                    print(verify)
                except:
                    return redirect('no_entreprise')
            conges =Demande_conges.objects.filter(reponse=False).count()
            return render(request, "admin/dashboard.html",{'conges':conges,'verify2':verify2,'verify':verify,'entrep':entrep,'entreprise':entreprise,'number_candidature':number_candidature,'number_recrut':number_recrut,'emp':emp})
        else:
            return redirect('index')
    else:
        return redirect('index')

def tables_data(request):
    return render(request, "admin/tables_data.html")


def tables_general(request):
    return render(request, "admin/tables_general.html")


class Pdf:
    def __init__(self,path):
        self.path = path

    def view_pdf(request,path):
        with open(path, 'rb') as pdf_file:
            response = FileResponse(pdf_file)
            return response



def candidat(request):
    if request.user.admin==True:
        candidat = Candidat.objects.filter(lu=False,supprimer=False)
        return render(request,'admin/candidat.html',{'candidat':candidat})
    else:
        return redirect('index')
    

def detailcandidat(request,pk):
    if request.user.admin==True:
        obj = get_object_or_404(Candidat,pk=pk)
        print(obj.nom)

        return render(request,'admin/detailcandidat.html',{'obj':obj})
    else:
        return redirect('index')

def candidatureValide(request):
    if request.user.admin==True:
        candidat = Candidat.objects.filter(lu=True,supprimer=False)
        return render(request,'admin/candidatureValide.html',{'candidat':candidat})
    else:
        return redirect('index')
    

# cette fonction permet de changer le statut d'une candidature en True
def lu(request,pk):
    if request.user.admin==True:
        obj = get_object_or_404(Candidat,pk=pk)
        obj.lu=True
        obj.save()
        return redirect('candidatureValide')
    else:
        return redirect('index')

def supprimer(request,pk):
    if request.user.admin==True:
        obj = get_object_or_404(Candidat,pk=pk)
        obj.supprimer = True
        obj.save()
        return redirect('candidat')
    else:
        return redirect('index')

def recruteur(request):
    if request.user.admin == True:
        candidat_ent = CandidatureEntreprise.objects.filter(lu=False,supprimer=False)
        return render(request,'admin/recruteur.html',{'candidat_ent':candidat_ent})
    else:
        return redirect('index')

def detailentreprise(request,pk):
    if request.user.admin==True:
        obj = get_object_or_404(CandidatureEntreprise,pk=pk)
        # print(obj.nom)
        return render(request,'admin/detailentreprise.html',{'obj':obj})
    else:
        return redirect('index')

def lectureEntreprise(request,pk):
    if request.user.admin==True:
        obj = get_object_or_404(CandidatureEntreprise,pk=pk)
        obj.lu=True
        obj.save()
        return redirect('recruteur')
    else:
        return redirect('index')

def supprimerentreprise(request,pk):
    if request.user.admin==True:
        obj = ''
        try:
            obj = get_object_or_404(CandidatureEntreprise,pk=pk)
        except:
            return redirect('entreprise')
        obj.supprimer = True
        obj.save()
        return redirect('candidat')
    else:
        return redirect('index')


def candidature_user(request):
    if request.user.is_authenticated:
        if request.user.admin == True:
            candidature_user=Candidat.objects.filter(lu=False,supprimer=False)
            return render(request,'admin/candidature_user.html',{'candidature_user':candidature_user})
        else:
            return redirect('index')
    else:
        return redirect('index')


def detailscandidature_user(request,pk):
    if request.user.is_authenticated:
        if request.user.admin==True:
            obj=''
            try:
                obj = get_object_or_404(Candidature,pk=pk)
            except:
                return redirect('offres')
            return render(request,'admin/detailscandidature_user.html',{'obj':obj})
        else:
            return redirect('index')
    else:
        return redirect('index')


def detail_entreprise(request,pk):
    if request.user.is_authenticated:
        if request.user.admin:
            obj=''
            try:
                obj = get_object_or_404(Entreprise,pk=pk)
                print(obj.gerant)
            except:
                return redirect('dashboard')
            return render(request,'admin/detail_entreprise.html',{'obj':obj})
        else:
            return redirect('index')
    else:
        return redirect('index')


class PDFWithImage(FPDF):
    def header(self):
        self.set_font('Arial', 'B', 12)
        self.cell(0, 10, 'En-tête du document', 0, 1, 'C')

    def add_image(self, image_path, x, y, width, height):
        self.image(image_path, x, y, width, height)




def fiche_employer(request):
    if request.user.is_authenticated:
        if request.user.travailleur == True:
            doc = Dokumente.objects.all()
            user_online = request.user
            obj =''
            try:
                obj = Employer.objects.get(nom=user_online)
            except:
                return redirect('no_access')
            verify = Masignature.objects.filter(employer=obj)
            if len(verify) == 0:
                return redirect('sig')
            wochentag=''
            datum=''
            arbeitszeit=''
            pause=''
            stunden=''
            employer =''
            heurejour=''
            entreprise=''
            stunden=0
            if request.method == 'POST':
                usere = request.user
                employer = Employer.objects.get(nom=usere)
                wochentag = request.POST.get('wochentag')
                datum = request.POST.get('datum')
                arbeitszeit1 = request.POST.get('arbeitszeit1')
                arbeitszeit2 = request.POST.get('arbeitszeit2')
                entreprise = request.POST.get('entreprise')
                cpt = 0
                heure_soumise =''
                heure_minimale = time(6, 0, 0)
                heure_debut = datetime.strptime(str(arbeitszeit1), '%H:%M').time()
                heure_fin = datetime.strptime(str(arbeitszeit2), '%H:%M').time()
                difference_heures = timedelta(hours=heure_fin.hour, minutes=heure_fin.minute) - timedelta(hours=heure_debut.hour, minutes=heure_debut.minute)
                heure_minimale = time(6, 0, 0)
                try:
                    heure_soumise = datetime.strptime(str(difference_heures), '%H:%M:%S').time()
                except:
                    messages.success(request,'Die Startzeit muss größer als die Endzeit sein')
                    return redirect('fiche_employer')
                pause =0

                if heure_soumise > heure_minimale:
                    print('pause ok')
                    pause =30
                    heure_utilisateur = str(heure_soumise)
                    heure_soumise2 = datetime.strptime(heure_utilisateur, '%H:%M:%S')
                    nouvelle_heure = heure_soumise2 - timedelta(minutes=30)
                    print('nvvvv',nouvelle_heure.time())
                    stundenf = str(nouvelle_heure.time())
                else:
                    print('pas de pause')
                    pause = 0
                    stundenf = str(difference_heures)
                verify = Compteur.objects.filter(employer=employer)
                datas = FicheEmployer.objects.create(
                    wochentag=wochentag,
                    datum=datum,
                    arbeitszeit1=arbeitszeit1,
                    arbeitszeit2=arbeitszeit2,
                    stunden=stundenf,
                    employer=employer,
                    pause = pause,

                    entreprise=entreprise

                    )
                # print(entreprise)

                datas.save()
                return redirect('fiche_employer')


            # emp = request.user?
            usere = request.user
            employer =''
            total = timedelta()
            try:
                employer = Employer.objects.get(nom=usere)
            except:
                messages.success(request,'Vous ne travaillez dans aucune entreprise')
                return redirect('index')


            # query0 = FicheEmployer.objects.filter(employer=employer,semaine=False)[:6]
            number_v = FicheEmployer.objects.filter(employer=employer,valider=False).count()
            # obj_ent = Entreprise.objects.get(nom_entreprise=entreprise)
            # entre_inst = obj_ent.nom_entreprise
            utilis= request.user
            entu = Employer.objects.filter(nom=utilis)

            me = request.user
            obj_user = Employer.objects.get(nom=me)
            query = FicheEmployer.objects.filter(employer=obj_user,valider = False)
            sumh=0
            signal =0
            summ =0
            convert_minut =0
            for row in query:
                print(row.stunden)
                sumh += row.stunden.hour
                summ +=row.stunden.minute
                convert_minut = summ / 60
            sumh = sumh + convert_minut
            if sumh > 36:
                hs = sumh-36
                me = request.user
                obj_me = Employer.objects.get(nom=me)
                hss = Heure_sup.objects.create(nh=hs,employer = obj_me)
                hss.save()
            else:
                pass
            try:
                sal = GriseSalariale.objects.all()[0]
            except:
                sal ="#"
                signal = signal+1
            return render(request,'admin/fiche_employer.html',{'doc':doc,'signal':signal,'sal':sal,'entu':entu,'query':query,'sumh':sumh})
        else:
            return redirect('index')
    else:
        return redirect('index')

def envoyer(request):
    pdf = FPDF('P', 'mm', 'A4')
    pdf.add_page()
    pdf.set_font('Arial', 'B', 10)
    pdf.cell(0, 10, 'KalenderWoche (Zeiterfassung)',0,1)

    pdf.set_font('Arial', 'B', 10)
    pdf.cell(0, 5, f'Name des Mitarbeiters: {request.user.username}',0,1)
            # pdf.cell(0, 10, '................................ ',0,1)
    me = request.user


    image_path = 'static/logo/kamga.jpg'
    pdf.image(image_path,80, 14, 68, 30)
    pdf.set_xy(150, 15)
    pdf.cell(0,0,'Paul Verlin Kamga')

    pdf.set_xy(150, 20)
    pdf.cell(0,0,'Zeitarbeitsunternehmer')

    pdf.set_xy(150, 25)
    pdf.cell(0,0,'+49 17 26 71 98 21')

    pdf.set_xy(150, 30)
    pdf.cell(0,0,'kontakt@kapver.com')

    pdf.set_xy(150, 35)
    pdf.cell(0,0,'Eichenstrasse 5, 47665 Sonsbeck')
    pdf.ln(1)


    pdf.set_font('Arial', 'B', 16)
    pdf.set_xy(10, 60)
    pdf.cell(0,0,'Vom Mitarbeiters auszufÜllen und vom kunden bestätigen lassen.')
    pdf.ln(8)
    pdf.set_font('Arial', 'B', 10)
    en_tetes = ["Wochentag", "Datum", "Arbeitszeit","pause","Stunden"]  # Remplacez par vos en-têtes
    obj_user = Employer.objects.get(nom=me)
    query = FicheEmployer.objects.filter(employer=obj_user,valider = False)
    total_heures = timedelta()
    for objet_exemple in query:
        # heure = stunden.hour
        total_heures += timedelta(hours=objet_exemple.stunden.hour, minutes=objet_exemple.stunden.minute, seconds=objet_exemple.stunden.second)

# total_heures contient maintenant la somme des heures de la liste
    query = FicheEmployer.objects.filter(employer=obj_user,valider = False)
    print(query,'wwe')
    for en_tete in en_tetes:
        pdf.cell(40, 10, en_tete, 1)
    pdf.ln()
    sumh=0
    summ =0
    entreprise =''
    for row in query:
        print(row.stunden)
        sumh += row.stunden.hour
        summ +=row.stunden.minute
        print('heure',row.arbeitszeit2.hour)
        pdf.cell(40, 10, str(row.wochentag), 1)
        pdf.cell(40, 10, str(row.datum), 1)
        pdf.cell(40, 10, str(f"{row.arbeitszeit1} - {row.arbeitszeit2}"), 1)
        pdf.cell(40, 10, str(row.pause),1)
        pdf.cell(40, 10, str(row.stunden), 1)
        entreprise = row.entreprise
            # pdf.cell(40, 10, str(row.heurejour), 1)
        pdf.ln()
    print('heure c',sumh)
    pdf.set_xy(10, 30)
    pdf.cell(0, 0, f'Kundenbetrieb : {entreprise}')
    print('somme minutes',summ)
    convert_minut = summ / 60
    sumh = sumh + convert_minut
    if sumh > 36:
        hs = sumh-36
        me = request.user
        obj_me = Employer.objects.get(nom=me)
        hss = Heure_sup.objects.create(nh=hs,employer = obj_me)
        hss.save()
    else:
        pass
    pdf.set_xy(150, 160)
    pdf.cell(0,0,f"Gesamtstunden: {sumh}")
    me = request.user
    obj_emp = Employer.objects.get(nom=me)
    list_user = Masignature.objects.filter(employer = obj_emp)[0]
    path_m =f"media/{list_user.sig}"
    pdf.set_xy(8, 145)
    pdf.cell(0,0,"Unterschrift Mitarbeiter :")
    import uuid

    pdf.image(path_m, x=2, y=150, w=80, h=20)
    identifiant = uuid.uuid4()
    print(identifiant)
    pdf.set_xy(8, 185)

    pdf.cell(0,0,"Unterschrift Kunden :")
    pdf.output(f'static/fiche/tuto1.pdf', 'F')
    chemin_pdf = 'static/fiche/tuto1.pdf'
    with open(chemin_pdf, 'rb') as fichier:
        document = Fiche()
        user = request.user
        employer = Employer.objects.get(nom=user)
        count = Fiche.objects.filter(employer=employer).count()
        if len(query) == 0:
            pass
        else:
            document.fiche.save('fichier_generé.pdf', File(fichier))
            document.employer= employer
            document.valider = True
            obj_ent = Entreprise.objects.get(nom_entreprise=entreprise)
            document.entreprise = obj_ent
                    # obj_ent = Entreprise.objects.get(nom_entreprise=entreprise)
                    # entre_inst = obj_ent.nom_entreprise
                    # document.entreprise=obj_ent

            document.save()
            for i in query:
                i.valider = True
                i.save()

        return redirect('fiche_employer')





def soumettre(request):
    if request.user.is_authenticated:
        if request.user.membre_staff == True:
            if request.user.travailleur == True:
                user = request.user
                employer = Employer.objects.get(nom=user)
                query = FicheEmployer.objects.filter(employer=employer,valider=False)
                for i in query:
                    i.valider = True
                    i.save()
                return redirect('fiche_employer')
            else:
                return redirect('index')
        else:
            return redirect("index")
    else:
        return redirect('index')


def facture(request):
    if request.user.is_authenticated:
        if request.user.admin == True:
            wochentag=''
            datum=''
            arbeitszeit=''
            pause=''
            stunden=''
            employer =''
            heurejour=''
            client=''
            query1=''
            if request.method == 'POST':
                usere = request.user
                employer = Employer.objects.get(nom=usere)
                wochentag = request.POST.get('wochentag')
                datum = request.POST.get('datum')
                arbeitszeit = request.POST.get('arbeitszeit')
                client=request.POST.get('client')
                pause = request.POST.get('pause')
                stunden = request.POST.get('stunden')
                heure_debut = datetime.strptime(arbeitszeit, '%H:%M')
                heure_fin = datetime.strptime(stunden, '%H:%M')
                resultat = heure_fin - heure_debut
                heurejour = str(resultat)

                # print('deded',resultat_str)
                datas = Ficheentreprise.objects.create(
                    wochentag=wochentag,
                    datum=datum,
                    arbeitszeit=arbeitszeit,
                   pause=pause,
                   stunden=stunden,
                   employer=employer,
                   heurejour=heurejour
                )
                datas.save()


            return render(request,'admin/facture.html')
        else:
            return redirect('index')
    else:
        return redirect('index')

def facture_client(request):
    if request.user.is_authenticated:
        if request.user.admin == True:

            return render(request,'admin/facture_client.html')
        else:
            return redirect('index')
    else:
        return redirect('index')


def detail_employer(request,pk):
    if request.user.is_authenticated:
        if request.user.admin == True:
            obj = Employer.objects.get(pk=pk)
            return render(request,'admin/detail_employer.html',{'obj':obj})
        else:
            return redirect('index')
    else:
        return redirect('index')

def fich_employer(request,pk):
    if request.user.is_authenticated:
        if request.user.admin == True:
            obj = Employer.objects.get(pk=pk)
            print(obj.pk)
            nome = obj.nom
            employer = Employer.objects.get(nom=nome)
            fich = Fiche.objects.filter(employer=employer)
            for i in fich:
                print(i.pk)
            return render(request,'admin/fich_employer.html',{'fich':fich})
        else:
            return redirect('index')
    else:
        return redirect('index')


def signature(request):
    if request.user.is_authenticated:
        if request.user.entreprise ==True:
            me = request.user
            obj_me = UserModel.objects.get(username=me)
            obj_entreprise = Entreprise.objects.get(gerant=me)
            verify_entrep = Signature.objects.filter(gerant=obj_me,entreprise=obj_entreprise)

            print(verify_entrep)
            if len(verify_entrep) == 0:
                if request.method == 'POST':
                    signature = request.FILES.get('signature')

                    mas = Signature.objects.create(signature=signature,gerant = obj_me,entreprise=obj_entreprise)
                    # mas.save()
                    print(request.POST)
            else:
                return redirect('dashboard')
            return render(request,'admin/signature.html')
        else:
            return redirect('index')
    else:
        return redirect('index')

def sig(request):
    if request.user.is_authenticated:
        if request.user.travailleur == True:
            user_online = request.user
            obj = Employer.objects.get(nom=user_online)
            verify = Masignature.objects.filter(employer=obj)
            if len(verify) == 0:
                # print(verify)
                if request.method =='POST':

                    sig = request.FILES.get('sig')
                    print('fefeferf',sig)
                    signature = Masignature.objects.create(sig=sig,employer=obj)
                    signature.save()
                    messages.success(request,'signature importée avec succès')
                    return redirect('fiche_employer')
            else:
                messages.success(request,'signature existante !')
            return render(request,'admin/sig.html')
        else:
            return redirect('index')
    else:
        return redirect('index')



def fiche_presence(request):
    if request.user.is_authenticated:
        if request.user.entreprise == True:
            mes_emp=''
            try:
                ent = Entreprise.objects.filter(gerant=request.user)[0]
                print('dfdfd',ent)
                ger = ent.nom_entreprise
                # print('sfdfd',ger)
                mes_emp = Fiche.objects.filter(entreprise=ent,valider=True,signer_entreprise=False)
                print(mes_emp,'wdedfefe')
                mes_emp2= Fiche.objects.filter(entreprise=ent,valider=True,signer_entreprise=True)

                # print(mes_emp)
            except:
                messages.success(request,'Entreprise non existante')
                return redirect('dashboard')
            return render(request,'admin/fiche_presence.html',{'mes_emp':mes_emp,'mes_emp2':mes_emp2})
        else:
            return redirect('index')
    else:
        return redirect('index')


from PyPDF2 import PdfReader, PdfWriter
from PIL import Image
from io import BytesIO
from django.http import FileResponse
import fitz
def signe_fiche(request, pk):
    if request.user.is_authenticated:
        if request.user.entreprise:
            obj = get_object_or_404(Fiche, pk=pk)
            src_pdf_filename = f'media/{obj.fiche}'
            dst_pdf_filename = f'media/{obj.fiche}'
            ger = request.user
            ma_sig =''
            try:
                ma_sig = Signature.objects.filter(gerant=ger)[0]
            except:
                messages.success(request,'signature non existente !')
                return redirect('fiche_presence')
            # print('fefrgrg',ma_sig)
            img_filename = f'media/{ma_sig.signature}'
            obj = Fiche.objects.get(pk=pk)
            existing_pdf_path = f"media/{obj.fiche}"
            url_img = 'static/logo/kamga.jpg'
            print(existing_pdf_path)
            img_rect = fitz.Rect(20,20, 250, 1100)

            document = fitz.open(src_pdf_filename)

            page = document[0]
            page.insert_image(img_rect, filename=img_filename)

            document.save(src_pdf_filename,incremental=True,encryption=0)
            obj.signer_entreprise=True
            maintenant = datetime.now()
            obj.date_signer_entreprise = maintenant
            obj.save()

            document.close()
            user = request.user
            # gerant_s = Entreprise.objects.get(gerant=user)
            # query = Signature.objects.select_related('entreprise').filter(gerant=gerant_s)
            # print(query)
            return redirect('fiche_presence')


        else:
            return redirect('index')
    else:
        return redirect('index')


def facturier(request):
    if request.method=='POST':
        bz= request.POST.get('bz')
        einheit = request.POST.get('einheit')
        menge = request.POST.get('menge')
        menge = menge.replace(',','.')
        einzelpreis = request.POST.get('einzelpreis')
        einzelpreis = einzelpreis.replace(',','.')
        user_online = request.user
        try:
            summe = float(einzelpreis) * float(menge)
            user = UserModel.objects.get(username=user_online)

            datas = Facturier.objects.create(bz=bz,einheit=einheit,menge=menge,einzelpreis=einzelpreis,user=user,summe=summe )
            return redirect('facturier')
        except:
            messages.success(request,"Bitte geben Sie reelle Zahlen ein !!")
            return redirect('facturier')
    query = Facturier.objects.filter(imprimer=False)
    query1 = Mesfactures.objects.all().order_by('date')
    return render(request,'admin/facturier.html',{'query':query,'query1':query1})



def impression(request):
    if request.user.is_authenticated:
        if request.user.admin == True:
            pdf = FPDF()
            pdf.add_page()
            # pdf.set_xy(150, 15)
            image_path = 'static/logo/kamga.jpg'
            pdf.image(image_path,170, 9, 30, 30)

            image_path = 'static/plan/paul.jpg'
            pdf.image(image_path,48, 120, 120, 60)

            image_path = 'static/icon/phone.png'
            pdf.image(image_path,20, 50, 4, 4)
            pdf.set_font('Arial', 'B', 11)
            pdf.set_xy(25, 50)
            pdf.cell(0,5,'01726719821',0,1)

            image_path = 'static/icon/mail.png'
            pdf.image(image_path,80, 50, 4, 4)
            pdf.set_xy(85, 50)
            pdf.cell(0,5,'kontakt@kapver.com',0,1)

            image_path = 'static/icon/position.jpg'
            pdf.image(image_path,140, 50, 4, 4)
            pdf.set_xy(145, 50)
            pdf.cell(0,5,'Eichenstr.5,47665 Sonsbeck',0,1)


            pdf.set_text_color(255, 0, 0)  # Rouge
            pdf.set_xy(9, 43)
            pdf.cell(0,0,'___________________________________________________________________________________',0,1)


            pdf.set_text_color(0, 0, 0)
            pdf.set_xy(15, 60)
            pdf.cell(0,5,'RECHNUNG AN:')

            pdf.set_xy(15, 65)
            pdf.cell(0,5,'Isselguss GmbH AN:')

            pdf.set_xy(15, 70)
            pdf.cell(0,5,'Minervastrasse 1,:')
            Rechnung=''
            Ausstellungsdatum=''
            Falligkeitsdatum=''
            Abteilung=''

            pdf.set_xy(15, 75)
            pdf.cell(0,5,'46419 Isselburg:')
            if request.method =='POST':
                Rechnung = request.POST.get('Rechnung')
                Ausstellungsdatum = request.POST.get('Ausstellungsdatum')
                Falligkeitsdatum = request.POST.get('Falligkeitsdatum')
                Abteilung = request.POST.get('Abteilung')

            pdf.set_xy(140, 60)
            pdf.cell(0,5,f'Rechnung Nr: {Rechnung}')

            pdf.set_xy(140, 65)
            pdf.cell(0,5,f'Ausstellungsdatum: {Ausstellungsdatum}')

            pdf.set_xy(140, 70)
            pdf.cell(0,5,f'Falligkeitsdatum: {Falligkeitsdatum}')

            pdf.set_xy(140, 75)
            pdf.cell(0,5,f'Abteilung: {Abteilung}')

            pdf.set_xy(15, 90)
            pdf.cell(0,0,'Sehr geehtrte Damen und Herren,')

            pdf.set_xy(15, 95)
            pdf.cell(0,0,'vielen Dank für Ihren Auftrag un das damit verbundene Vertrauen')

            pdf.set_xy(15, 100)
            pdf.cell(0,0,'Hiermit stelle ich die folgenden Leistungen in Rechnung')
            pdf.ln()
            en_tetes = ["POS", "BZ.", "Einheit","Menge","Einzelpreis","Summe"]
            total=0
            # for en_tete in en_tetes:
            #     pdf.cell(50, 10, en_tete[0], border=0)
            pdf.set_xy(15, 110)
            pdf.cell(0,0,en_tetes[0])
            pdf.set_xy(45, 110)
            pdf.cell(0,0,en_tetes[1])

            pdf.set_xy(100, 110)
            pdf.cell(0,0, en_tetes[2])
            pdf.set_xy(130, 110)
            pdf.cell(0,0, en_tetes[3])
            pdf.set_xy(160, 110)
            pdf.cell(0,0, en_tetes[4])

            pdf.set_xy(185, 110)
            pdf.cell(0,0, en_tetes[5])
            # pdf.cell(0,0, en_tetes[1])
            # pdf.cell(50,10, en_tetes[2])
            # pdf.cell(50,10, en_tetes[3])
            # pdf.cell(50,10, en_tetes[4])
            # pdf.cell(50,10, en_tetes[5])

            query = Facturier.objects.filter(imprimer=False)
            pdf.ln()
            cpt = 0
            total = 0
            eur = '€'
            x = 0
            y = 110
            max_menge_digits = 0
            max_einzelpreis_digits = 0
            max_summe_digits=0

            for row in query:
                menge_str = str(row.menge)
                einzelpreis_str = str(row.einzelpreis)
                summe_str = str(round(row.summe, 2))

                if '.' in menge_str:
                    digits_before_decimal = menge_str.index('.')
                    if digits_before_decimal > max_menge_digits:
                        max_menge_digits = digits_before_decimal

                if '.' in einzelpreis_str:
                    digits_before_decimal = einzelpreis_str.index('.')
                    if digits_before_decimal > max_einzelpreis_digits:
                        max_einzelpreis_digits = digits_before_decimal

                if '.' in summe_str:
                    digits_before_decimal = summe_str.index('.')
                    if digits_before_decimal > max_summe_digits:
                        max_summe_digits = digits_before_decimal

            # Step 4: Iterate over the query and display formatted .menge values
            for row in query:
                cpt = cpt + 1
                summe = row.summe
                total += round(row.summe, 2)

                pdf.ln(20)
                pdf.set_xy(15, y + 10)
                pdf.cell(0, 0, str(cpt), border=0)

                pdf.ln()
                # Colonne 2
                pdf.set_xy(45, y + 10)
                pdf.multi_cell(0, 0, str(row.bz), border=0)
                pdf.ln()
                # Colonne 3
                pdf.set_xy(100, y + 10)
                pdf.multi_cell(0, 0, str(row.einheit), border=0)
                pdf.ln()
                # Colonne 4
                # Calculate the number of digits before the decimal point in the current .menge value
                menge_str = str(row.menge)
                if '.' in menge_str:
                    digits_before_decimal = menge_str.index('.')
                else:
                    digits_before_decimal = len(menge_str)

                # Adjust the x position based on the difference between the maximum digits and current digits
                x = 130 + (max_menge_digits - digits_before_decimal) * 2
                pdf.set_xy(x, y + 10)
                pdf.multi_cell(0, 0, str(row.menge), border=0)
                pdf.ln()
                # Colonne

                einzelpreis_str = str(row.einzelpreis)
                if '.' in einzelpreis_str:
                    digits_before_decimal = einzelpreis_str.index('.')
                else:
                    digits_before_decimal = len(einzelpreis_str)

                # Adjust the x position based on the difference between the maximum digits and current digits
                x = 160 + (max_einzelpreis_digits - digits_before_decimal) * 2
                pdf.set_xy(x, y + 10)

                pdf.multi_cell(0, 0, str(row.einzelpreis), border=0)
                pdf.ln()
                # Colonne 6

                summe_str = str(row.summe)
                if '.' in summe_str:
                    digits_before_decimal = summe_str.index('.')
                else:
                    digits_before_decimal = len(summe_str)

                # Adjust the x position based on the difference between the maximum digits and current digits
                x = 185 + (max_summe_digits - digits_before_decimal) * 2
                pdf.set_xy(x, y + 10)

                summe = round(summe, 2)
                pdf.multi_cell(50, 0, str(summe), border=0)

                # Increment the value of y to move to the next line
                y += 10

                row.imprimer = True
                row.save()
                pdf.ln()


            pdf.ln(10)
            pdf.set_xy(0, 190)
            pdf.cell(0, 0, '________________________________________________________________________________________________________________________________________________')
            pdf.set_font('Arial', 'B', 10)
            pdf.set_xy(15, 195)
            pdf.cell(0,0,"Summe")
            print('dfdfdf',total)
            pdf.set_xy(185, 195)
            total = round(total,2)
            pdf.cell(0,0,f"{total}")
            pdf.set_xy(0, 198)
            pdf.cell(0, 0, '________________________________________________________________________________________________________________________________________________')




            pdf.set_xy(140, 205)
            pdf.cell(0,0,"USt")

            pdf.set_xy(160, 205)
            pdf.cell(0,0,"19%")
            taxef = total * 19
            taxe = taxef / 100
            taxe = round(taxe,2)

            pdf.set_xy(185, 205)
            pdf.cell(0,0,f"{taxe}")

            montant = total+taxe
            montant = round(montant,2)
            pdf.set_xy(140, 215)
            pdf.cell(0,0,"Gesamtbetrag: ")
            pdf.set_xy(185, 215)
            pdf.cell(0,0,f"{montant}")
            pdf.set_font('Arial', 'B', 10)
            pdf.set_xy(130, 220)
            pdf.cell(0,0,"______________________________________________")
            pdf.ln(1)
            pdf.set_font('Arial', 'I', 8)
            pdf.set_font('Arial', 'I', 8)
            pdf.set_xy(15, 230)
            pdf.cell(0,0,"Bitte überweisen Sie den Rechnungsbetrag unter Angabe der Rechnungsnummer auf das unten angegebene konto. ")
            pdf.set_xy(15,235)
            pdf.cell(0,0,f'Der Rechnungsbetrag ist am {Falligkeitsdatum} fällig')

            pdf.set_xy(35,255)
            pdf.cell(0,0,'Paul Kamga Personnalvermittlung')
            pdf.set_xy(35,260)
            pdf.cell(0,0,'Eichenstrasse 5, 47665 Sonsbeck')
            pdf.set_xy(35,265)
            pdf.cell(0,0,'E-mail : Kapver.kontakt@gmail.com')
            pdf.set_xy(35,270)
            pdf.cell(0,0,'Betnr: 75353317/ Stnr: 119/5145/2997')
            pdf.set_xy(35,275)
            # pdf.cell(0,0,'Betnr: 75353317/ Stnr: 119/5145/2997')

            pdf.set_xy(130,255)
            pdf.cell(0,0,'Geschäftsführer: Paul Verlin Kamga')
            pdf.set_xy(130,260)
            pdf.cell(0,0,'UStnr: In bearbeitung')
            pdf.set_xy(130,265)
            pdf.cell(0,0,'Kreditsinstitut: Commerzbank')
            pdf.set_xy(130,270)
            pdf.cell(0,0,'IBAN: DE56 3204 0024 0812 4349 00')
            pdf.set_xy(130,275)
            pdf.cell(0,0,'BLZ: 32040024')



            pdf.output('static/mesfactures/tuto1.pdf', 'F')
            chemin_pdf = 'static/mesfactures/tuto1.pdf'

            with open(chemin_pdf, 'rb') as fichier:
                document = Mesfactures()
                on_line = request.user
                user = UserModel.objects.get(username=on_line)
                document.mesfactures.save('mesfacture.pdf', File(fichier))
                document.user = user
                document.save()
            # pdf.set_xy(0, 269)
            # pdf.cell(0,0,"Bitte Uberweisen Sie Rechnungsbertrag unter Angabe der Rechnungsnummer auf das angegebene Konto . ")
            # pdf.output("tableau_horizontal.pdf")

            return redirect('facturier')
        else:
            return redirect('index')
    else:
        return redirect('index')



def no_access(request):

    return render(request,'admin/no_access.html')


def no_entreprise(request):
    return render(request,'admin/no_access.html')

def email(request):
    return render(request,'admin/email.html')


def mescollaborations(request):
    if request.user.is_authenticated:
        if request.user.admin == True:
            if request.method == 'POST':
                nom = request.POST.get('nom')
                code_pays = request.POST.get('code_pays')
                numero = request.POST.get('numero')
                email = request.POST.get('email')
                adresse = request.POST.get('adresse')
                verify = Collaborateur.objects.filter(nom=nom)
                if len(verify) == 0:
                    datas = Collaborateur.objects.create(nom=nom,numero=numero,email=email,adresse=adresse,code_pays=code_pays)
                    messages.success(request,'Mitarbeiter mit Erfolg speichern')

                    return redirect('mescollaborations')
                else:
                    messages.success(request,'cet collaborateur existe deja !!')
                    return redirect('mescollaborations')
            query = Collaborateur.objects.all()
            return render(request,'admin/mescollaborations.html',{'query':query})
        else:
            return redirect('dashboard')
    else:
        return redirect('index')


# def sendemail(request,pk):
#     if request.user.is_authenticated:
#         if request.user.admin == True:
#             if request.method =='POST':
#                 obj = get_object_or_404(Collaborateur,pk=pk)
#                 email = request.POST.get('email')
#                 message = request.POST.get('message')
#                 objects = request.POST.get('objects')
#                 filef = request.FILES.get('file')

#                 dest = settings.EMAIL_HOST_USER
#                 # new_mail.add_html_file('./kapver_app/templates/admin/mytamplateemail.html')
#                 html_message = render_to_string('admin/mytamplateemail.html',{'message':message})
#                 # new_mail.attach_files(filef)
#                 plain_message = strip_tags(html_message)
#                 mail.send_mail(objects, plain_message, dest, [email], html_message=html_message)

#                 # print(new_mail)
#                 # new_mail.send(settings.EMAIL_HOST_PASSWORD)
#             return render(request,'admin/email.html')
#         else:
#             return redirect('dashboard')
#     else:
#         return redirect('index')

def mytamplateemail(request):
    if request.user.is_authenticated:
        if request.user.admin == True:
            return render(request,'admin/mytamplateemail.html')
        else:
            return redirect('dashboard')
    else:
        return redirect('index')








from django.shortcuts import render, get_object_or_404, redirect
from django.core.mail import EmailMessage, EmailMultiAlternatives
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from django.conf import settings

def sendemail(request, pk):
    if request.user.is_authenticated:
        collaborateur=''
        if request.user.admin:
            collaborateur = get_object_or_404(Collaborateur, pk=pk)
            if request.method == 'POST':

                email = request.POST.get('email')
                message = request.POST.get('message')
                objects = request.POST.get('objects')
                filef = request.FILES.get('file')

                dest = settings.EMAIL_HOST_USER

                # Créez un objet EmailMultiAlternatives pour le format texte brut et HTML
                email_message = EmailMultiAlternatives(
                    objects,  # Sujet de l'e-mail
                    strip_tags(message),  # Corps de l'e-mail (version texte brut)
                    dest,  # Adresse e-mail de l'expéditeur
                    [email],  # Liste des destinataires
                )

                # Ajoutez le message HTML (corps de l'e-mail au format HTML)
                html_message = render_to_string('admin/mytamplateemail.html', {'message': message})
                email_message.attach_alternative(html_message, 'text/html')

                # Attachez la pièce jointe au courriel si elle est fournie
                if filef:
                    email_message.attach(filef.name, filef.read(), filef.content_type)

                # Envoyez l'e-mail
                # try:
                email_message.send()
                messages.success(request,'Mail erfolgreich versendet')
                return redirect('sendemail',pk=pk)
                # except Exception as e:
                    # messages.error(request,'Email not sent:',str(e))
                    # E-Mail nicht gesendet. Ausfall der Internetverbindung

            return render(request, 'admin/email.html',{'collaborateur':collaborateur})  # Créez un formulaire d'envoi d'e-mail
        else:
            return redirect('dashboard')
    else:
        return redirect('index')


def changesalaire(request,pk):
    if request.user.is_authenticated:
        if request.user.admin == True:
            obj =get_object_or_404(Facturier,pk=pk)
            if request.method == 'POST':
                bz= request.POST.get('bz')
                einheit = request.POST.get('einheit')
                menge = request.POST.get('menge')
                menge = menge.replace(',','.')



                einzelpreis = request.POST.get('einzelpreis')
                einzelpreis = einzelpreis.replace(',','.')

                pourcentage = request.POST.get('pourcentage')
                pourcentage = pourcentage.replace(',','.')
                pourcentage = float(pourcentage)
                summe = float(einzelpreis)*float(menge)*float(pourcentage) / 100
                # summe = summe*
                print('summeee',summe)
                user = request.user
                obj_user = UserModel.objects.get(username=user)
                infosfacture = Facturier.objects.create(einheit=einheit,menge=menge,einzelpreis=einzelpreis,summe=summe,user=obj_user,bz=bz)
                infosfacture.save()

            return render(request,'admin/changesalaire.html',{'obj':obj})
            # except:
            #     return redirect('facturier')
        else:
            return redirect('dashboard')
    else:
        return redirect('index')


def deletemesfactures(request,pk):
    if request.user.is_authenticated:
        if request.user.admin == True:
            obj =get_object_or_404(Facturier,pk=pk)
            obj.delete()
            return redirect('facturier')
            messages.success(request,'facture supprimer avec success')
        else:
            return redirect('dashboard')
    else:
        return redirect('index')


def view_pdf2(request, pk):
    document = get_object_or_404(Client, pk=pk)

    # Lecture du fichier PDF
    with document.mesfactures.open('rb') as pdf_file:
        response = HttpResponse(pdf_file.read(), content_type='application/pdf')
        response['Content-Disposition'] = 'inline; filename="' + document.cv.name + '"'
        return response

def travailleur1(request):
    if request.user.is_authenticated:
        user = UserModel.objects.filter(username=request.user)
        for i in user:
            i.travailleur =True
            i.entreprise = False
            i.admin = False
            i.save()
            return redirect('fiche_employer')


def admin1(request):
    if request.user.is_authenticated:
        user = UserModel.objects.filter(username=request.user)
        for i in user:
            i.admin =True
            i.travailleur =False
            i.entreprise = False
            i.save()
            return redirect('dashboard')


def entreprise1(request):
    if request.user.is_authenticated:
        user = UserModel.objects.filter(username=request.user)
        for i in user:
            i.entreprise =True
            i.travailleur = False
            i.admin= False
            i.save()
            return redirect('dashboard')

import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

logger = logging.getLogger(__name__)

logger = logging.getLogger(__name__)

def sendfacture(request, pk):
    logger.debug('Début de la fonction sendfacture')

    if request.user.is_authenticated:
        if request.user.admin:
            obj = get_object_or_404(Mesfactures, pk=pk)
            logger.debug(f'Objet récupéré: {obj}')

            if request.method == 'POST':
                recipient_email = request.POST.get('email')
                message = request.POST.get('message')
                objects = request.POST.get('objects')
                filel = request.FILES.get('file')
                
                logger.debug(f'E-mail du destinataire: {recipient_email}')

                try:
                    file_content = obj.mesfactures.read()
                    file_name = obj.mesfactures.name

                    if filel:
                        file_contentl = filel.read()
                        file_namel = filel.name
                        content_typel, _ = mimetypes.guess_type(file_namel)
                    else:
                        file_contentl = file_namel = content_typel = None

                    content_type, _ = mimetypes.guess_type(file_name)

                    email = EmailMessage(
                        subject=objects,
                        body=message,
                        to=[recipient_email],
                    )

                    if file_content:
                        email.attach(filename=file_name, content=file_content, mimetype=content_type)
                    if file_contentl:
                        email.attach(filename=file_namel, content=file_contentl, mimetype=content_typel)
                    
                    html_message = render_to_string('admin/mytamplateemail.html', {'message': message})
                    email.content_subtype = "html"
                    email.body = html_message

                    logger.debug('Envoi de l\'e-mail')
                    email.send()
                    logger.debug('E-mail envoyé avec succès')

                    messages.success(request, 'Datei erfolgreich gesendet')
                    return redirect('facturier')

                except Exception as e:
                    logger.error(f'Erreur lors de l\'envoi de l\'e-mail: {str(e)}')
                    return HttpResponseServerError("Une erreur s'est produite lors de l'envoi de l'e-mail : {}".format(str(e)))

            logger.debug('Méthode HTTP non POST, affichage du formulaire')
            return render(request, 'admin/sendfacture.html', {'obj': obj})

        else:
            logger.debug('L\'utilisateur n\'est pas un administrateur, redirection vers index')
            return redirect('index')

    else:
        logger.debug('L\'utilisateur n\'est pas authentifié, redirection vers login')
        return redirect('accounts/login')

def essaie(request):
    subject = "Test d'envoi d'email"
    message = "Ceci est un test d'envoi d'email via le serveur SMTP d'OVH."
    to_email = "thierry.devp@gmail.com"

    send_email(subject, message, to_email)
    return redirect('dashboard')



from django.core.mail import EmailMessage
from django.http import HttpResponseServerError
import mimetypes


def view_pdf2(request, pk):
    document = get_object_or_404(Mesfactures, pk=pk)

    # Lecture du fichier PDF
    with document.mesfactures.open('rb') as pdf_file:
        response = HttpResponse(pdf_file.read(), content_type='application/pdf')
        response['Content-Disposition'] = 'inline; filename="' + document.mesfactures.name + '"'
        return response

def voirpdf(request, pk):
    document = get_object_or_404(Fiche, pk=pk)

    # Lecture du fichier PDF
    with document.fiche.open('rb') as pdf_file:
        response = HttpResponse(pdf_file.read(), content_type='application/pdf')
        response['Content-Disposition'] = 'inline; filename="' + document.fiche.name + '"'
        return response


def voirgrisesalarial(request, pk):
    document = get_object_or_404(GriseSalariale, pk=pk)

    # Lecture du fichier PDF
    with document.fichier.open('rb') as pdf_file:
        response = HttpResponse(pdf_file.read(), content_type='application/pdf')
        response['Content-Disposition'] = 'inline; filename="' + document.fichier.name + '"'
        return response

def voirdokumente(request, pk):
    document = get_object_or_404(Dokumente, pk=pk)

    # Lecture du fichier PDF
    with document.doc.open('rb') as pdf_file:
        response = HttpResponse(pdf_file.read(), content_type='application/pdf')
        response['Content-Disposition'] = 'inline; filename="' + document.doc.name + '"'
        return response

def voirfiche(request, pk):
    document = get_object_or_404(Employer, pk=pk)

    # Lecture du fichier PDF
    with document.fiche.open('rb') as pdf_file:
        response = HttpResponse(pdf_file.read(), content_type='application/pdf')
        response['Content-Disposition'] = 'inline; filename="' + document.fiche.name + '"'
        return response


def bilden(request):
    if request.user.is_authenticated:
        if request.user.admin ==True:
            query = Fiche.objects.filter(valider=True,signer_entreprise=True,approuver=False)
            return render(request,'admin/bilden.html',{'query':query})
        else:
            return redirect('dashboard')
    else:
        return redirect('index')



def dokumente(request):
    if request.user.is_authenticated:
        if request.user.admin ==True:
            query = Dokumente.objects.all()
            return render(request,'admin/dokumente.html',{'query':query})
        else:
            return redirect('dashboard')
    else:
        return redirect('index')


def voirfichesig(request, pk):
    document = get_object_or_404(Fiche, pk=pk)

    # Lecture du fichier PDF
    with document.fiche.open('rb') as pdf_file:
        response = HttpResponse(pdf_file.read(), content_type='application/pdf')
        response['Content-Disposition'] = 'inline; filename="' + document.fiche.name + '"'
        return response


def approuver(request,pk):
    if request.user.is_authenticated:
        if request.user.admin == True:
            obj = get_object_or_404(Fiche,pk=pk)
            obj.approuver = True
            obj.save()
            return redirect('bilden')
        else:
            return redirect('dashboard')
    else:
        return redirect('index')


def sendfiche(request, pk):
    if request.user.is_authenticated:
        if request.user.admin:
            obj = get_object_or_404(Fiche, pk=pk)

            if request.method == 'POST':
                recipient_email = request.POST.get('email')
                message = request.POST.get('message')
                objects = request.POST.get('objects')
                filel = request.FILES.get('file')
                file_contentl=''
                file_namel=''
                content_typel=''

                try:
                    # Récupérer le fichier stocké dans Mesfactures
                    file_content = obj.fiche.read()  # Suppose que votre champ de fichier est nommé "fiche"
                    file_name = obj.fiche.name  # Nom du fichier
                    if filel:
                        file_contentl=file_contentl = filel.read()
                        file_namel = filel.name
                        content_typel, _ = mimetypes.guess_type(file_namel)

                    # Déterminer le type de contenu du fichier à partir de son nom de fichier
                    content_type, _ = mimetypes.guess_type(file_name)

                    # Créer un objet EmailMessage pour l'e-mail
                    email = EmailMessage(
                        subject=objects,
                        body=message,
                        to=[recipient_email],
                    )

                    # Attacher le fichier à l'e-mail
                    email.attach(filename=file_name, content=file_content, mimetype=content_type)
                    email.attach(filename=file_namel, content=file_contentl, mimetype=content_typel)
                    html_message = render_to_string('admin/mytamplateemail.html', {'message': message})
                    email.content_subtype = "html"  # Définit le type de contenu comme HTML
                    email.body = html_message  # Définit le corps de l'e-mail comme le message HTML

                    # Envoyer l'e-mail
                    email.send()

                    # Rediriger ou renvoyer une réponse appropriée après l'envoi de l'e-mail
                    # Par exemple, rediriger vers une page de confirmation
                    messages.success(request,'Datei erfolgreich gesendet')
                    return redirect('bilden')

                except Exception as e:
                    # Gérer les exceptions lors de l'envoi de l'e-mail
                    return HttpResponseServerError("Une erreur s'est produite lors de l'envoi de l'e-mail : {}".format(str(e)))

            # Si la méthode HTTP n'est pas POST, afficher le formulaire avec les détails de l'objet Mesfactures
            return render(request, 'admin/sendfacture.html', {'obj': obj})

        else:
            return redirect('index')

    else:
        return redirect('accounts/login')


def ficheapprouver(request):
    if request.user.is_authenticated:
        if request.user.admin == True:
            query = Fiche.objects.filter(valider=True,signer_entreprise=True,approuver=True)
            return render(request,'admin/ficheapprouver.html',{'query':query})
        else:
            return redirect('dashboard')
    else:
        return redirect('index')


def conges(request):
    if request.user.is_authenticated and request.user.travailleur:
        entreprise =''
        verify=''
        if request.method == 'POST':  # Überprüfen Sie, ob das Formular gesendet wurde
            name = request.POST.get('name')
            geb = request.POST.get('geb')
            personalnummer = request.POST.get('personalnummer')
            von = request.POST.get('von')
            bis = request.POST.get('bis')
            resturlaub = request.POST.get('resturlaub')
            diesesjahr = request.POST.get('diesesjahr')
            datum_antrag = request.POST.get('datum_antrag')
            unterschrift_arbeitnehmer = request.POST.get('unterschrift_arbeitnehmer')
            begrundung_arbeitgeber = request.POST.get('begrundung_arbeitgeber')
            # unterschrift_arbeitgeber = request.POST.get('unterschrift_arbeitgeber')
            entreprise = request.POST.get('entreprise')
            datum_des_antrag = request.POST.get('datum_des_antrag')
            user = request.user
            obj_user = Employer.objects.filter(nom=user)
            verify_entrep = Entreprise.objects.filter(nom_entreprise=entreprise)
            print('entrepse',verify_entrep)
            nom_ent=''
            ent=''
            get_entreprise=''
            if len(verify_entrep) != 0:
                ent   = Entreprise.objects.get(nom_entreprise=entreprise)
            if len(obj_user) != 0:
                obj_user = Employer.objects.get(nom=user)
                print('user',obj_user)
            else:
                return redirect('conges')
            pdf= FPDF()
            pdf.add_page()
            pdf.image("kapver_app/kamga.jpg", x=15, y=5, w=47, h=25)

            pdf.set_font('ARIAL', 'B', 15)
            pdf.set_xy(150, 8)
            pdf.cell(0, 0, 'P a u l  K a m g a')

            pdf.set_font('ARIAL', '', 11)
            pdf.set_xy(150, 12)
            pdf.cell(0, 0, 'Personalvermittlung')

            pdf.set_font('ARIAL', '', 11)
            pdf.set_xy(158, 16)
            pdf.cell(0, 0, 'Eichenstr. 5')

            pdf.set_font('ARIAL', '', 11)
            pdf.set_xy(156, 20)
            pdf.cell(0, 0, '47665 Sonsbeck')

            pdf.set_xy(150, 24)
            pdf.cell(0, 0, 'Fon +49 172 67 19 821')


            pdf.set_font('ARIAL', '', 11)
            pdf.set_xy(86, 29)
            pdf.cell(0, 0, 'An den Arbeitgeber')

            pdf.set_font('ARIAL', 'B', 15)
            pdf.set_xy(86, 46)
            pdf.cell(0, 0, 'Urlaubsantrag')

            pdf.set_font('ARIAL', '', 11)
            pdf.set_xy(15, 60)
            pdf.cell(0, 0, 'Name, Vorname: ')

            pdf.set_font('ARIAL', '', 11)
            pdf.set_xy(45, 60)
            pdf.cell(0, 0, ' ........................................................')

            pdf.set_xy(45, 59)
            pdf.cell(0, 0, f' {name}')

            pdf.set_font('ARIAL', '', 11)
            pdf.set_xy(15, 68)
            pdf.cell(0, 0, 'Geb. am: ')

            pdf.set_font('ARIAL', '', 11)
            pdf.set_xy(33, 68)
            pdf.cell(0, 0, ' ..................................')

            pdf.set_xy(33, 67)
            pdf.cell(0, 0, f'{geb}')

            pdf.set_font('ARIAL', '', 11)
            pdf.set_xy(15, 75)
            pdf.cell(0, 0, 'Personalnummer: ')

            pdf.set_font('ARIAL', '', 11)
            pdf.set_xy(45, 75)
            pdf.cell(0, 0, ' .............................')

            pdf.set_xy(45, 74)
            pdf.cell(0, 0, f' {personalnummer}:')

            pdf.set_font('ARIAL', 'B', 11)
            pdf.set_xy(15, 82)
            pdf.cell(0, 0, 'Betreff: ')

            pdf.set_font('ARIAL', '', 11)
            pdf.set_xy(29, 82)
            pdf.cell(0, 0, '  Urlaubsantrag')

            pdf.set_font('ARIAL', '', 11)
            pdf.set_xy(15, 97)
            pdf.cell(0, 0, 'Hiermit beantrage ich Urlaub vom')

            pdf.set_font('ARIAL', '', 11)
            pdf.set_xy(73, 98)
            pdf.cell(0, 0, ' .....................')

            pdf.set_xy(74, 97)
            pdf.cell(0, 0, f'{von}')

            pdf.set_font('ARIAL', '', 11)
            pdf.set_xy(98, 97)
            pdf.cell(0, 0, '[Datum] bis ')

            pdf.set_font('ARIAL', '', 11)
            pdf.set_xy(118, 97)
            pdf.cell(0, 0, ' ...................')

            pdf.set_xy(118, 96)
            pdf.cell(0, 0, f' {bis}')

            pdf.set_font('ARIAL', '', 11)
            pdf.set_xy(140, 97)
            pdf.cell(0, 0, '[Datum].')

            pdf.set_font('ARIAL', '', 11)
            pdf.set_xy(15, 103)
            pdf.cell(0, 0, 'Bei meinen Urlaubstagen handelt es sich um')

            pdf.set_font('ARIAL', '', 11)
            pdf.set_xy(92, 103)
            pdf.cell(0, 0, ' ..................')

            pdf.set_xy(92, 102)
            pdf.cell(0, 0, f' {resturlaub}')

            pdf.set_font('ARIAL', '', 11)
            pdf.set_xy(112, 103)
            pdf.cell(0, 0, 'Tage aus dem Vorjahr (Resturlaub)')

            pdf.set_font('ARIAL', '', 11)
            pdf.set_xy(15, 110)
            pdf.cell(0, 0, ' ......................')

            pdf.set_xy(15, 109)
            pdf.cell(0, 0, f' {diesesjahr}')

            pdf.set_font('ARIAL', '', 11)
            pdf.set_xy(41, 110)
            pdf.cell(0, 0, 'und um')

            pdf.set_font('ARIAL', '', 11)
            pdf.set_xy(54, 110)
            pdf.cell(0, 0, ' ..................................')

            pdf.set_xy(54, 109)
            pdf.cell(0, 0, f'{datum_antrag}')

            pdf.set_font('ARIAL', '', 11)
            pdf.set_xy(92, 110)
            pdf.cell(0, 0, 'Tage aus diesem Jahr.')

            pdf.set_font('ARIAL', '', 11)
            pdf.set_xy(15, 137)
            pdf.cell(0, 0, '............................')

            pdf.set_font('ARIAL', '', 11)
            pdf.set_xy(15, 142)
            pdf.cell(0, 0, '[Datum des Antrags]')

            pdf.set_font('ARIAL', '', 11)
            pdf.set_xy(15, 135)
            pdf.cell(0, 0, f'{datum_des_antrag}')



            pdf.set_font('ARIAL', '', 11)
            pdf.set_xy(15, 160)
            pdf.cell(0, 0, '(Unterschrift des Arbeitnehmers)')

            pdf.set_font('ARIAL', '', 11)
            pdf.set_xy(15, 175)
            pdf.cell(0, 0, ' ..................................................................................................................................................................................')

            pdf.set_xy(15, 174)
            pdf.cell(0,0,f'{unterschrift_arbeitnehmer}')

            pdf.set_font('ARIAL', '', 11)
            pdf.set_xy(15, 178)
            pdf.cell(0, 0, ' ..................................................................................................................................................................................')

            pdf.set_font('ARIAL', 'B', 11)
            pdf.set_xy(92, 200)
            pdf.cell(0, 0, 'Antwort des Arbeitgebers')

            pdf.set_font('ARIAL', '', 11)
            pdf.set_xy(15, 210)
            pdf.cell(0, 0, 'Der beantragte Urlaub wird bewilligt /abgelehnt, weil')

            pdf.set_font('ARIAL', '', 11)
            pdf.set_xy(105, 210)
            pdf.cell(0, 0, '............................................')

            pdf.set_xy(105, 209)
            pdf.cell(0, 0, '.')

            pdf.set_font('ARIAL', 'B', 11)
            pdf.set_xy(15, 218)
            pdf.cell(0, 0, '[Begründung des Arbeitgebers].')

            pdf.set_font('ARIAL', '', 11)
            pdf.set_xy(15, 245)
            pdf.cell(0, 0, '..................................')

            pdf.set_xy(15, 244)
            pdf.cell(0, 0, '.')

            pdf.set_font('ARIAL', '', 11)
            pdf.set_xy(15, 252)
            pdf.cell(0, 0, '(Unterschrift des Arbeitgebers)')

            from django.core.files.base import ContentFile
            date_actuelle = datetime.now()
            #enregistrer le pdf
            # pdf.output('factur1.pdf', 'F')
            pdf.output(f'media/demande/Urlaubsantrag_{request.user}_{date_actuelle}.pdf', 'F')
            chemin_pdf = f'media/demande/Urlaubsantrag_{request.user}_{date_actuelle}.pdf'
            with open(chemin_pdf, 'rb') as fichier:
                document = Demande_conges()
                # document.demande.save('Urlaubsantrag.pdf', File(fichier))
                # contenu_fichier = fichier.read()
                # fichier_content = ContentFile(contenu_fichier)
                document.demande=f'demande/Urlaubsantrag_{request.user}_{date_actuelle}.pdf'


                get_entre = Entreprise.objects.get(nom_entreprise=entreprise)
                print('entreprise',get_entre)
                me = request.user
                obj_user = Employer.objects.get(nom=me)
                document.employer=obj_user
                document.entreprise=get_entre
                print('user 1',obj_user)
                document.save()
                messages.success(request,'Ihre Anfrage wurde erfolgreich gesendet')
                return redirect('fiche_employer')
        user = request.user
        user_on=request.user
        verify = Employer.objects.filter(nom=user_on)
        print('hello',verify)
        return render(request, 'admin/conges.html',{'verify':verify})  # Zeigen Sie das Formular an, wenn es ein GET-Anforderung ist

    else:
        return redirect('index')  # Benutzer umleiten, wenn nicht authentifiziert oder kein Arbeitnehmer



def test(request):
    return render(request,'admin/test.html')

def conges_travailleur(request):
    if request.user.is_authenticated:
        if request.user.entreprise == True:
            me = request.user
            query=''
            get_entre = Entreprise.objects.filter(gerant=me)
            if len(get_entre) !=0:
                get_entre = Entreprise.objects.filter(gerant=me)[0]
                query= Demande_conges.objects.filter(entreprise=get_entre,reponse=False)
                print(query)
            else:
                return redirect('no_access')

            return render(request,'admin/conges_travailleur.html',{'query':query})
        else:
            return redirect('dashboard')
    else:
        return redirect('accounts/login')


def voirdemande(request, pk):
    document = get_object_or_404(Demande_conges, pk=pk)

    # Lecture du fichier PDF
    with document.demande.open('rb') as pdf_file:
        response = HttpResponse(pdf_file.read(), content_type='application/pdf')
        response['Content-Disposition'] = 'inline; filename="' + document.demande.name + '"'
        return response



from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from django.utils.html import strip_tags

def send_email_with_attachment_and_html(subject, message, recipient_list, attachment_path, html_template):
    """
    Fonction pour envoyer un e-mail avec une pièce jointe et une page HTML en utilisant Django.

    Args:
        subject (str): Objet du message.
        message (str): Corps du message.
        recipient_list (list): Liste des destinataires.
        attachment_path (str): Chemin vers la pièce jointe.
        html_template (str): Chemin vers le modèle HTML.
        context (dict): Contexte contenant les données à passer au modèle HTML.

    Returns:
        bool: True si l'e-mail a été envoyé avec succès, False sinon.
    """
    try:
        # Rendu du modèle HTML
        html_content = render_to_string(html_template)

        # Conversion en texte brut
        text_content = strip_tags(html_content)

        # Création de l'e-mail
        email = EmailMultiAlternatives(
            subject=subject,
            body=text_content,
            from_email=None,  # Utilisera DEFAULT_FROM_EMAIL défini dans les paramètres de votre projet Django
            to=recipient_list,
        )

        # Ajout du contenu HTML
        email.attach_alternative(html_content, "text/html")

        # Ajout de la pièce jointe
        with open(attachment_path, 'rb') as attachment:
            email.attach('nom_piece_jointe.pdf', attachment.read(), 'application/pdf')

        # Envoi de l'e-mail
        email.send()

        return True
    except Exception as e:
        # En cas d'erreur lors de l'envoi de l'e-mail
        print(f"Erreur lors de l'envoi de l'e-mail : {e}")
        return False






from io import BytesIO
from reportlab.pdfgen import canvas
from PyPDF2 import PdfReader, PdfWriter
from django.shortcuts import get_object_or_404
from django.http import HttpResponse
from django.shortcuts import render, redirect

def reponse_demande(request, pk):
    if request.user.entreprise and request.user.is_authenticated:
        if request.method=='POST':
            obj_demande = get_object_or_404(Demande_conges, pk=pk)

            # Chemin vers le fichier PDF
            chemin_pdf = obj_demande.demande.path

            # Ouvrir le fichier PDF en mode lecture-binaire
            with open(chemin_pdf, "rb") as pdf_file:
                # Créer un objet PdfReader pour lire le contenu du PDF
                reader = PdfReader(pdf_file)

                # Créer un objet PdfWriter pour écrire dans le PDF
                writer = PdfWriter()

                # Récupérer la première page du PDF
                page = reader.pages[0]

                # Définir les coordonnées où vous souhaitez ajouter le texte
                coord_x = 50
                coord_y = 147

                coordo_x = 310
                coordo_y = 250
                textarea1  = request.POST.get('textarea1')
                textarea2 = request.POST.get('textarea2')

                # Créer un BytesIO pour stocker le PDF généré par ReportLab
                buffer = BytesIO()

                # Créer un canvas ReportLab pour écrire du texte sur la page
                can = canvas.Canvas(buffer)
                can.drawString(coord_x, coord_y, f"{textarea2}")
                can.drawString(coordo_x, coordo_y, f"{textarea1}")
                can.save()
                obj_demande.reponse = True


                # Ajouter le contenu du canvas ReportLab à la première page du PDF existant
                new_pdf = PdfReader(buffer)
                text_page = new_pdf.pages[0]
                page.merge_page(text_page)

                # Ajouter la première page modifiée au writer
                writer.add_page(page)
                med='media'
                # Ajouter les pages restantes du PDF original au writer
                for num_page in range(1, len(reader.pages)):
                    writer.add_page(reader.pages[num_page])

                # Écrire le contenu modifié dans un nouveau fichier PDF
                chemin_nouveau_pdf = f"{med}/demande/Urlaubsantrag.pdf"

                with open(chemin_nouveau_pdf, "wb") as output_pdf:
                    writer.write(output_pdf)

                # Mettre à jour le champ demande de l'objet Demande_conges avec le chemin du nouveau fichier PDF
                obj_demande.demande = "demande/Urlaubsantrag.pdf"
                obj_demande.save()

                messages.success(request,'Antwort erfolgreich gesendet')
                subject = "Antwort auf den Urlaubsantrag"
                message = f"Hallo {obj_demande.employer} Anbei finden Sie unser Feedback zu Ihrem Urlaubsantrag. Aufrichtig !"
                recipient_list = [f"{obj_demande.employer.nom.email}", "kontakt@kapver.com"]
                attachment_path = chemin_nouveau_pdf
                html_template = 'admin/mytamplateemail.html'
                # context = {'name': 'John Doe', 'message': 'Bonjour!'}

                send_email_with_attachment_and_html(subject, message, recipient_list, attachment_path, html_template)


                return redirect('conges_travailleur')

        return render(request, 'admin/reponse_demande.html')
    else:
        return redirect('index')















