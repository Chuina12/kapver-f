from django.db import models
from django.contrib.auth.models import AbstractUser
from ckeditor.fields import RichTextField




class UserModel(AbstractUser):
    travailleur = models.BooleanField(default=False)
    entreprise = models.BooleanField(default=False)
    admin = models.BooleanField(default=False)
    membre_staff = models.BooleanField(default=False)

    class Meta:
        verbose_name = ('UserModel')
        verbose_name_plural = ('UserModels')
    def __str__(self):
        return self.username



class Candidature(models.Model):
    intitule = models.CharField(max_length=100,blank=True,null=True)
    nom = models.CharField(max_length=100)
    message = models.TextField()
    cv = models.FileField(upload_to='cv')
    date = models.DateTimeField(auto_now_add=True,blank=True,null=True)

    def __str__(self):
        return self.nom +'' + self.message
    class Meta:
        verbose_name= ('Candidature')
        verbose_name_plural = ('Candidatures')


class CandidatureEntreprise(models.Model):
    entreprise = models.CharField(max_length=100)
    phone = models.IntegerField()
    domain = models.CharField(max_length=100)
    adresse_email = models.EmailField(null=True,blank=True)
    adresse = models.CharField(max_length=100)
    message = models.TextField()
    date = models.DateTimeField(auto_now_add=True)
    lu = models.BooleanField(default=False)
    supprimer = models.BooleanField(default=False)

    class  Meta:
        verbose_name = ('CandidatureEntreprise')
        verbose_name_plural = ('CandidatureEntreprises')

    def __str__(self):
        return self.entreprise



class Offre(models.Model):
    domain = models.CharField(max_length=100)
    entreprise = models.CharField(max_length=100,blank=True,null=True)
    lieu = models.CharField(max_length=100,blank=True,null=True)
    nombre_heure = models.IntegerField(blank=True,null=True)
    titre = models.CharField(max_length=100)
    description = RichTextField()  # Utilisation de CKEditor ici
    date = models.DateTimeField(auto_now_add=True)
    expiration = models.BooleanField(default=False)
    def __str__(self):
        return self.titre
    class  Meta:
        verbose_name = ('Offre')
        verbose_name_plural = ('Offres')


class Candidat(models.Model):
    offre = models.ForeignKey(Offre,on_delete=models.CASCADE)
    nom = models.CharField(max_length=100)
    message = models.TextField()
    cv = models.FileField(upload_to='cv')
    date  = models.DateTimeField(auto_now_add=True)
    lu = models.BooleanField(default=False)
    supprimer = models.BooleanField(default=False)

    def __str__(self):
        return self.nom
    class Meta:
        verbose_name = ('Candidat')
        verbose_name_plural = ('Candidats')


class Entreprise(models.Model):
    gerant = models.ForeignKey(UserModel,on_delete=models.CASCADE,related_name='partenaire')
    nom_entreprise  = models.CharField(max_length=100)
    date  = models.DateTimeField(auto_now_add=True)
    adresse = models.CharField(max_length=100)
    email = models.EmailField()
    BP = models.CharField(max_length=100)
    nombre_travailler = models.IntegerField(null=True,blank=True)


    def __str__(self):
        return f"{self.nom_entreprise}"
    class Meta:
        verbose_name= ('Entreprise')
        verbose_name_plural = ('Entreprises')


class Employer(models.Model):
    nom = models.ForeignKey(UserModel,on_delete=models.CASCADE,related_name='nom_employer')
    entreprise = models.ForeignKey(Entreprise,on_delete=models.CASCADE,related_name='entreprseE')
    date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.nom}"

    class Meta:
        verbose_name= ('Employer')
        verbose_name_plural = ('Employers')


class FicheEmployer(models.Model):
    employer = models.ForeignKey(Employer,on_delete=models.CASCADE,null=True,blank=True)
    wochentag =models.CharField(max_length=100)
    datum = models.DateField(auto_now_add=True)
    arbeitszeit1 = models.TimeField(blank=True, null=True)
    arbeitszeit2 = models.TimeField(blank=True, null=True)
    pause = models.IntegerField(blank=True, null=True)
    stunden = models.TimeField(blank=True, null=True)
    entreprise = models.CharField(max_length=100,blank=True, null=True)
    valider = models.BooleanField(default=False)
    heure_sp = models.FloatField(blank=True, null=True)



    def __str__(self):
        return f"{self.employer}"
    class Meta:
        verbose_name=('FicheEmployer')
        verbose_name_plural  = ('FicheEmployers')


class Fiche(models.Model):
    fiche = models.FileField(upload_to='fiche/', null=True, blank=True)
    date = models.DateTimeField(auto_now_add=True)
    valider = models.BooleanField(default=False)
    signer_entreprise = models.BooleanField(default=False)
    signer_employer = models.BooleanField(default=False)
    employer = models.ForeignKey(Employer, related_name='emp', on_delete=models.CASCADE,blank=True,null=True)
    entreprise = models.ForeignKey(Entreprise,on_delete=models.CASCADE,blank=True,null=True)
    date_signer_entreprise = models.DateTimeField(blank=True, null=True)
    date_signer_employer = models.DateTimeField(blank=True, null=True)
    approuver = models.BooleanField(default=False)
    def __str__(self):
        return f"{self.employer}"



    class Meta:
        verbose_name = ('Fiche')
        verbose_name_plural = ('Fiches')

class Facture(models.Model):
    # user  = models.ForeignKey(UserModel, on_delete=models.CASCADE)
    client  = models.CharField(max_length = 150)
    date = models.DateTimeField(auto_now_add=True)
    facture = models.FileField(upload_to='facture',blank=True, null=True)


    def __str__(self):
        return self.client

    class Meta:
        verbose_name=('Facture')
        verbose_name_plural = ('Factures')



class Ficheentreprise(models.Model):
    employer = models.ForeignKey(Employer,on_delete=models.CASCADE,null=True,blank=True)
    wochentag =models.CharField(max_length=100)
    datum = models.DateField(auto_now_add=True)
    arbeitszeit = models.TimeField()
    stunden = models.TimeField()
    heurejour = models.TimeField(null=True,blank=True)
    valider = models.BooleanField(default=False)


    def __str__(self):
        return f"{self.employer}"
    class Meta:
        verbose_name=('Ficheentreprise')
        verbose_name_plural  = ('Ficheentreprises')


class Heure_sup(models.Model):
    nh = models.FloatField()
    employer =  models.ForeignKey(Employer, on_delete=models.CASCADE)
    date = models.DateTimeField(auto_now_add=True,blank=True, null=True)

    def __str__(self):
        return self.employer.nom.username

    class Meta:
        verbose_name = ('Heure_sup')
        verbose_name_plural = ('Heure_sups')

class Compteur(models.Model):
    employer  = models.OneToOneField(Employer,on_delete=models.CASCADE,blank=True, null=True)
    cpt = models.IntegerField()
    date = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name=('Compteur')
        verbose_name_plural = ('Compteurs')


class Signature(models.Model):
    signature = models.ImageField(upload_to='signature')
    entreprise= models.OneToOneField(Entreprise,on_delete=models.CASCADE)
    date = models.DateTimeField(auto_now_add=True)
    gerant = models.ForeignKey(UserModel,on_delete = models.CASCADE,blank=True, null=True)


    def __str__(self):
        return self.entreprise.nom_entreprise

    class Meta:
        verbose_name = ('Signature')
        verbose_name_plural = ('Signatures')



class Facturier(models.Model):
    bz = models.CharField(max_length=100)
    einheit = models.CharField(max_length=100)
    menge =models.FloatField()
    einzelpreis = models.FloatField()
    date = models.DateField(auto_now_add=True)
    imprimer = models.BooleanField(default=False)
    summe = models.FloatField(blank=True, null=True)
    user = models.ForeignKey(UserModel, on_delete=models.CASCADE,blank=True, null=True)
    fiche = models.FileField(upload_to='facturier',blank=True, null=True)


    # @property
    # def getproduit(self):
    #     self.summe = self.menge * self.einzelpreis
    #     return self.summe
    def __str__(self):
        return self.bz
    class Meta:
        verbose_name = ('Facturier')
        verbose_name_plural = ('Facturiers')


class Mesfactures(models.Model):
    user = models.ForeignKey(UserModel, on_delete=models.CASCADE,blank=True, null=True)
    mesfactures = models.FileField(upload_to='mesfactures')
    date = models.DateTimeField(auto_now_add=True)
    confirm = models.BooleanField(default=False)

    def __str__(self):
        return self.user.username

    class Meta:
        verbose_name=('Mesfactures')
        verbose_name_plural = ('Mesfactures')


class Masignature(models.Model):
    sig = models.ImageField(upload_to='signature_travailleur')
    employer =  models.OneToOneField(Employer,on_delete=models.CASCADE)
    date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.employer.nom.username

    class Meta:
        verbose_name=('Masignature')
        verbose_name_plural = ('Masignatures')


class GriseSalariale(models.Model):
    fichier = models.FileField(upload_to='salaire')
    date = models.DateTimeField(auto_now_add = True)

    def __str__(self):
        return str(self.date)

class Collaborateur(models.Model):
    nom = models.CharField(max_length=100)
    email = models.EmailField()
    adresse = models.CharField(max_length=100)
    numero = models.IntegerField()
    code_pays = models.CharField(max_length=100)
    date = models.DateTimeField(auto_now_add = True,blank=True, null=True)

    def __str__(self):
        return self.nom

    class Meta:
        verbose_name = ('Collaborateur')
        verbose_name_plural = ('Collaborateurs')

class Dokumente(models.Model):
    name= models.CharField(max_length=100)
    doc = models.FileField(upload_to='dokument')
    date = models.DateTimeField(auto_now_add = True)

    def __str__(self):
        return self.name
    class Meta:
        verbose_name=('Dokumente')
        verbose_name_plural = ('Dokumentes')


class Conge(models.Model):
    employer = models.ForeignKey(Employer,on_delete=models.CASCADE)
    name = models.CharField(max_length=100, verbose_name='Name, Vorname')
    geb = models.DateField(verbose_name='Geb. am')
    personalnummer = models.CharField(max_length=100, verbose_name='Personalnummer')
    von = models.DateField(verbose_name='Urlaubsantrag vom')
    bis = models.DateField(verbose_name='bis')
    resturlaub = models.CharField(max_length=100,verbose_name='Tage aus dem Vorjahr (Resturlaub)')
    diesesjahr = models.IntegerField(verbose_name='Tage aus diesem Jahr')
    datum_antrag = models.DateField(verbose_name='Datum des Antrags')
    unterschrift_arbeitnehmer = models.CharField(max_length=100, verbose_name='Unterschrift des Arbeitnehmers')
    begrundung_arbeitgeber = models.TextField(verbose_name='Antwort des Arbeitgebers')
    unterschrift_arbeitgeber = models.CharField(max_length=100, verbose_name='Unterschrift des Arbeitgebers')
    entreprise = models.ForeignKey(Entreprise,on_delete=models.CASCADE,blank=True, null=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Conge'
        verbose_name_plural = 'Conges'


class Demande_conges(models.Model):
    demande = models.FileField(upload_to='demande')
    employer  = models.ForeignKey(Employer,on_delete=models.CASCADE)
    entreprise = models.ForeignKey(Entreprise,on_delete=models.CASCADE)
    date = models.DateField(auto_now_add=True)
    reponse = models.BooleanField(default=False)

    class Meta:
        verbose_name = ('Demande_conge')
        verbose_name_plural = ('Demande_conges')


class Kapver_info(models.Model):
    nom = models.CharField(max_length=255)
    image = models.ImageField(upload_to='kapver_info', blank=True, null=True)
    specialisation = RichTextField()
    recrutement_international = RichTextField()
    critere = RichTextField(null=True, blank=True)

    def __str__(self):
        return self.nom
    

class Banniere1(models.Model):
    titre = models.CharField(max_length=500)
    image_caroussel1 = models.ImageField(upload_to='caroussel1', null=True, blank=True)
    description = RichTextField()

    def __str__(self):
        return f"{self.titre}"

class Banniere2(models.Model):
    titre = models.CharField(max_length=500)
    image_caroussel2 = models.ImageField(upload_to='caroussel2', null=True, blank=True)
    description1 = RichTextField()
    description2 = RichTextField()

    def __str__(self):
        return f"{self.titre}"
