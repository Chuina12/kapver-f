from django.urls import path,include
from . import views
from django.views.generic import RedirectView


urlpatterns = [
    path('',views.index,name='index'),
    path('employeur',views.employeur,name='employeur'),
    path('candidature',views.candidature,name='candidature'),
#    path('contact',views.contact,name='contact'),
    path('offres',views.offres,name='offres'),
    path('conditions',views.conditions,name='conditions'),
    path('details/<int:pk>',views.details,name='details'),
    path('candidature_email', views.candidature_email, name='candidature_email'),

    #path for admin spaces
    path("dashboard", views.dashboard, name="dashboard"),
    path("dashboard/tables_data", views.tables_data, name="tables_data"),
    path("dashboard/tables_general", views.tables_general, name="tables_general"),
    path('candidat',views.candidat,name='candidat'),
    path('detailcandidat/<int:pk>',views.detailcandidat,name='detailcandidat'),
    path('candidatureValide', views.candidatureValide, name='candidatureValide'),
    path('lu/<int:pk>',views.lu,name='lu'),
    path('detailentreprise/<int:pk>',views.detailentreprise,name='detailentreprise'),
    path('supprimer/<int:pk>',views.supprimer,name='supprimer'),
    path('recruteur',views.recruteur,name='recruteur'),
    path('lectureEntreprise/<int:pk>',views.lectureEntreprise,name='lectureEntreprise'),
    path('supprimerentreprise/<int:pk>',views.supprimerentreprise,name='supprimerentreprise'),
    path('candidature_user',views.candidature_user,name='candidature_user'),
    path('detailscandidature_user/<int:pk>',views.detailscandidature_user,name='detailscandidature_user'),
    path('detail_entreprise/<int:pk>',views.detail_entreprise,name='detail_entreprise'),
    path('fiche_employer',views.fiche_employer,name='fiche_employer'),
    path('soumettre',views.soumettre,name='soumettre'),
    path('facture',views.facture,name='facture'),
    path('detail_employer/<int:pk>',views.detail_employer,name='detail_employer'),
    path('fich_employer/<int:pk>',views.fich_employer,name='fich_employer'),
    # path('fiche_employer',views.fiche_employer,name='fiche_employer')
    path('signature',views.signature,name='signature'),
    path('fiche_presence',views.fiche_presence,name='fiche_presence'),
    path('signe_fiche/<int:pk>',views.signe_fiche,name='signe_fiche'),
    path('facturier',views.facturier,name='facturier'),
    path('impression',views.impression,name='impression'),
    # path('ma_signature',views.ma_signature,name='ma_signature'),
    path('sig',views.sig,name='sig'),
    path('no_access',views.no_access,name='no_access'),
    path('no_entreprise',views.no_entreprise,name='no_entreprise'),
    path('envoyer',views.envoyer,name='envoyer'),
    path('email',views.email,name='email'),
    path('mescollaborations',views.mescollaborations,name='mescollaborations'),
    path('sendemail/<int:pk>',views.sendemail,name='sendemail'),
    path('mytamplateemail',views.mytamplateemail,name='mytamplateemail'),
    path('changesalaire/<int:pk>',views.changesalaire,name='changesalaire'),
    path('deletemesfactures/<int:pk>',views.deletemesfactures,name='deletemesfactures'),
    path('i18n/', include('django.conf.urls.i18n')),
    path('set_language/', RedirectView.as_view(url='/'), name='set_language'),
    path('view_pdf2/<int:pk>',views.view_pdf2,name='view_pdf2'),
    path('travailleur1',views.travailleur1,name='travailleur1'),
    path('admin1',views.admin1,name='admin1'),
    path('entreprise1',views.entreprise1,name='entreprise1'),
    # ...
    path('essaie',views.essaie,name='essaie'),
    path('sendfacture/<int:pk>',views.sendfacture,name='sendfacture'),
    path('view_pdf2/<int:pk>',views.view_pdf2,name='view_pdf2'),
    path('voirpdf/<int:pk>',views.voirpdf,name='voirpdf'),
    path('bilden',views.bilden,name='bilden'),
    path('voirfichesig/<int:pk>',views.voirfichesig,name='voirfichesig'),
    path('approuver/<int:pk>',views.approuver,name='approuver'),
    path('sendfiche/<int:pk>',views.sendfiche,name='sendfiche'),
    path('ficheapprouver',views.ficheapprouver,name='ficheapprouver'),
    path('dokumente',views.dokumente,name='dokumente'),
    path('voirdokumente/<int:pk>',views.voirdokumente,name='voirdokumente'),
    path('voirgrisesalarial/<int:pk>',views.voirgrisesalarial,name='voirgrisesalarial'),
    path('conges',views.conges,name='conges'),
    path('test',views.test,name='test'),
    path('conges_travailleur',views.conges_travailleur,name='conges_travailleur'),
    path('voirdemande/<int:pk>',views.voirdemande,name='voirdemande'),
    path('reponse_demande/<int:pk>',views.reponse_demande,name='reponse_demande')



]