/* Script complementaire  de l'algorithme version Cobalt 
Creer par Malik 19 Novembre 2021
*/

//Gestion de survol reponse item

var items=[];
function assertion_click(e){
  e.preventDefault();
  var item=$(`#asert${e.data.value}`);
  item.removeClass('bg-light');
  item.removeClass('text-secondary');
  item.addClass('bg-info');
  item.addClass('text-white');
  item.addClass('selected-item');
  if(e.data.choix_unique){
  for(var i=0; i<items.length; i++){
    const div = document.querySelector(items[i]);
    if(!div.classList.contains('selected-item')){;
    //if !$(items[i]).hasClass('selected-item'){}
     //$(items[i]).addClass('disabled');
    //}
    $(items[i]).addClass('disabled');
  }
  }
}
}
function assertion_hover(e){
  e.preventDefault();
  var item=$(`#asert${e.data.value}`);
  item.addClass('border border-info')
  
}
function assertion_leave(e){
  e.preventDefault();
  var item=$(`#asert${e.data.value}`);
  item.removeClass('border border-info')
  
}
//---------------
//------------//-----------------------
/*-------retirer une question de la liste--------------------*/
/*---------------//----------------------------------------*/
function load_question(data){
  var current=data.q_numero;
  var nomber=data.nbr_q;
  var q_name=data.q_name;
  var q_text=data.q_text;
  //console.log(data.q_text);
  var q_type=data.q_type;
  var repList=data.reponses;
  var replistBox=$("#rep-liste-box");
  var media_url=$("#skip").attr('url');
  var q_image=data.q_image
  var skip_block=$("#skip");
  //var header=$("#h-question");
  var qNameBx=$("#qName-box");
  var externalBox=$("#external");
  var imagebox=$("#q-image-block");
  replistBox.empty();
  qNameBx.empty();
  //header.empty();
  imagebox.empty();
  externalBox.empty();

  //$("#titleQ").text(`Q-> : ${q_text.slice(0,200)}`);
  $('#titleQ').empty();
  if (typeof(q_text) != "string" ){
      for(var i=0;i<q_text.length;i++){
          if(data.trou_liste){
              if(i == q_text.length-1){
              $("#titleQ").append(`
        ${q_text[i]}`)
          }else{
          $("#titleQ").append(`
        ${q_text[i]} <select style="width:10%;height:35px" class="custom-select form-control p-0 d-inline" id="inputGroupSelect04">\
              <option selected>Select...</option>\
              <option value="1">marcher</option>\
              <option value="2">chasser</option>\
              <option value="3">manger</option>\
            </select>`)}
          }else{
          if(i == q_text.length-1){
              $("#titleQ").append(`
        ${q_text[i]}`)
          }else{
          $("#titleQ").append(`
        ${q_text[i]} <input type="text" style="width:10%;" class="d-inline-block ">`)}
      }
      }
         
}else{
          $("#titleQ").text(`Q-> : ${q_text.slice(0,200)}`);
}
          
  
  if( data.q_image){
  imagebox.append(`<img style="width: 20%" src="${media_url}${data.q_image}"/>`)
}
  qNameBx.append(`<i class="fab fa-jenkins fa-3x"></i> ${q_name}`);
  if(data.q_external){
    externalBox.append(`<a href=${data.q_external}><i class="fas fa-external-link-alt"></i>${data.q_external}</a>`)
  }
  skip_block.attr("value",current);
  //data.nbr_q,data.q_name,data.q_type,data.q_text,data.q_image,data.q_external,data.reponses
  var counter=$("#number_of_q");
  counter.empty();
  counter.append(`<i class="fas fa-exclamation-circle text-warning"></i> Question N<sup>o</sup> ${current}/${nomber}, ${data.cote} points.`)
  //traitement de l'affichage des reponse en fonction du typt

  //Si multi choice
  if(data.q_type == "multichoice"){
    //affichage des reponse multi choice
    if(data.short_answer){}else{
    replistBox.append(`
        <div class="row">\
          <span>Cochez la ou les bonnes reponses:</span>\
          <div classe="col-md-12" id="reponse-box"></div>\
        </div>
      `)
    for(var i=0; i<repList.length;i++){
      $("#reponse-box").append(`
        <div class="row">\
        <a href="#" type='button' id="asert${i}" class="btn col-md-2 text-center text-secondary item bg-light p-2 m-1 mt-1 mb-2">${repList[i].text}</a>\
        <div class="col-md-2 text-center text-secondary d-none p-2 mt-1 mb-2">Vrai</div>\
        </div>
        `);
      if(data.choix_unique){$(`#asert${i}`).on('click',{value:i,choix_unique:true},assertion_click);}
      else{$(`#asert${i}`).on('click',{value:i,choix_unique:false},assertion_click);}
      $(`#asert${i}`).on('mouseenter',{value:i},assertion_hover);
      $(`#asert${i}`).on('mouseleave',{value:i},assertion_leave);
      items.push(`#asert${i}`)
  }
  }
  }
  //Si spell
  else if(data.q_type == "spellanswer"){

    replistBox.append(`
        <div class="row">\
          <span class="col-md-12">Saisissez votre reponse:</span>\
          <div class="input-group col-md-4 mb-3">\
            <input type="text" style="width:10%;" class="d-inline-block ">\
          </div>\
        </div>\
      `)

  }
  //numerical
  else if(data.q_type == "numerical"){
    replistBox.append(`
        <div class="row">\
          <span class="col-md-12">Saisissez votre reponse(du type numeric):</span>\
          <div class="input-group col-md-4 mb-3">\
            <input type="text" style="width:10%;" class="d-inline-block ">\
          </div>\
        </div>\
      `)
  }
  //close a reponse fermer
  if(data.q_type == "cloze"){
    //affichage des reponse multi choice
    if(data.true_libre){

      replistBox.append(`
        <div class="row">\
          <span>Remplissez les cases vide:<br/>------------------</span>\
          <div classe="col-md-12" id="reponse-box"></div>\
        </div>
      `)
      $("#reponse-box").append(`
        <div class="row">\
        Un chasseur sachant &nbsp;&nbsp; \
            <input type="text" style="width:7%;" class="d-inline-block">\
         &nbsp;&nbsp;sans son &nbsp;&nbsp;<input type="text" style="width:10%;" class="d-inline-block " >\
        &nbsp;&nbsp;est un bon &nbsp;&nbsp;\
            <input type="text" style="width:7%;" class="d-inline-block ">\
            ;&nbsp;la mort n'est <input type="text" style="width:7%;" class="d-inline-block">\&nbsp;mais vivre vaincu et sans <input type="text" style="width:10%;" class="d-inline-block">\
            c'est <input type="text" style="width:7%;" class="d-inline-block">\ pour toujouts.
        </div>
        `)

    }else if(data.true_liste){

      replistBox.append(`
        <div class="row">\
          <span>Selectionner une reponse pour chaque case vide<br/>---------------</span>\
          <div classe="col-md-12" id="reponse-box"></div>\
        </div>
      `)

      $("#reponse-box").append(`
        <div class="row">\
        Un chasseur sachant &nbsp;&nbsp; \
            <select style="width:10%;height:35px" class="custom-select form-control p-0 d-inline" id="inputGroupSelect04">\
              <option selected>Select...</option>\
              <option value="1">marcher</option>\
              <option value="2">chasser</option>\
              <option value="3">manger</option>\
            </select>\
         &nbsp;&nbsp;sans son &nbsp;&nbsp;<select style="width:10%;height:35px" class="custom-select form-control p-0 d-inline m-1" id="inputGroupSelect04">\
              <option selected>Select...</option>\
              <option value="1">One</option>\
              <option value="2">Two</option>\
              <option value="3">Three</option>\
            </select>\
        &nbsp;&nbsp;est un bon &nbsp;&nbsp;\
            <select style="width:10%;height:35px" class="custom-select form-control p-0 d-inline m-1" id="inputGroupSelect04">\
              <option selected>Select...</option>\
              <option value="1">One</option>\
              <option value="2">Two</option>\
              <option value="3">Three</option>\
            </select>\
            ;&nbsp;la mort n'est <select style="width:10%;height:35px" class="custom-select form-control p-0 d-inline m-1" id="inputGroupSelect04">\
              <option selected>Select...</option>\
              <option value="1">One</option>\
              <option value="2">Two</option>\
              <option value="3">Three</option>\
            </select>\&nbsp;mais vivre vaincu et sans <select style="width:10%;height:35px" class="custom-select form-control p-0 d-inline m-1" id="inputGroupSelect04">\
              <option selected>Select...</option>\
              <option value="1">One</option>\
              <option value="2">Two</option>\
              <option value="3">Three</option>\
            </select>\
            c'est <select style="width:10%;height:35px" class="custom-select form-control p-0 d-inline m-1" id="inputGroupSelect04">\
              <option selected>Select...</option>\
              <option value="1">One</option>\
              <option value="2">Two</option>\
              <option value="3">Three</option>\
            </select>\ pour toujouts.
        </div>
        `)

    }else{
    replistBox.append(`
        <div class="row">\
          <!--<span>Cochez la bonne reponse:</span>-->\
          <div classe="col-md-12" id="reponse-box"></div>\
        </div>
      `)
    for(var i=0; i<repList.length;i++){
      $("#reponse-box").append(`
        <div class="row">\
        <div class="col-md-2 text-center text-secondary bg-light p-3 m-1 mt-1 mb-2">${repList[i].text}</div>\
        <div class="col-md-2 text-center text-secondary d-none p-3 mt-1 mb-2">Vrai</div>\
        </div>
        `)
   }
 }
  }
  //Short answer(ecrire une reponse a la question)
   else if(data.q_type == "shortanswer"){

    replistBox.append(`
        <div class="row">\
          <span class="col-md-12">Saisissez la reponse:</span>\
          <div class="input-group col-md-4 mb-3">\
            <input type="text" style="width:10%;" class="d-inline-block ">\
          </div>\
        </div>\
      `)

  }
  //question a association
  else if(data.q_type == "matching"){
    var tab=["AAA","BBB","CCC","DDD"]
    replistBox.append(`
        <div class="row">\
          <span>Associez les box:</span>\
          <div classe="col-md-12" id="reponse-box"></div>\
        </div>
      `)
    for(var i=0; i<4;i++){
      $("#reponse-box").append(`
        <div class="row">\
        <div class="col-md-2 text-center text-secondary bg-light p-1 m-1 mt-1 mb-2">${tab[i]}</div>\
        <div class="col-md-2 border border-info text-center text-secondary p-1 mt-1 mb-2"></div>\
        </div>
        `)
    }
      $("#reponse-box").append(`
        <div class="row" id="drg">\
        </div>
        `)
      for(var i=0; i<4;i++){
        $("#drg").append(`
        <div class="col-md-1 text-center text-secondary bg-light p-1 m-1 mt-1">${tab[i]}</div>
        `)
      

  }
  }
}


function skip_question(e){
  e.preventDefault();
  var current_q=$("#skip").attr('value');
  var 
  data=new FormData()
  data.append("driven_quiz",true);
  data.append("current_q",current_q);
  data.append("action","next");
  data.append(
          "csrfmiddlewaretoken",
          $("input[name=csrfmiddlewaretoken]").val()
        );

  $.ajax({
    type: "POST",
    url:'',
    data:data,
    cache:false,
    processData:false,
    contentType:false,
    success: function(data){
      if(data.success_message){
        notify(data.success_message+ "<i class='fas fa-smile-beam text-warning'></i>",'success',delay=5000);
        load_question(data);
      }
      else{
        notify("Votre session de connexion a expirer.",'error',delay=5000)
        window.setTimeout(function () {
                window.location = "../";
              }, 5000);
      }
    },
    error: function (error){
      notify("Impossible de contacter le serveur, verifier votre connexion et reessayez.",'error');
    },
    async: true,
    timeout: 60000,
  });
  
}
$('#skip').on('click', skip_question);

/*---------------------load niveau--------------*/
function load_niveau(e){
  e.preventDefault();
  var niveau=$('#niveau-field').val();
  var niveauBox=$('#niveau-block');
  if( niveau.length >=2 ){
    niveauBox.text(niveau);
  }
  else{
    alert("Vous devez renseigner un niveu")
  }
}
$('#niveau-btn').on('click', load_niveau);
/*----------//---------------------------------*/
/*-----------select question--------------------*/

function choose_q(event){
  event.preventDefault();
  var question_id=$('#slct-question').val();
  var selectedBox=$('#selected-q-box');
  var question_text=$('#slct-question').find("option:selected").text();
  var option_selected=$('#slct-question').find("option:selected");
  
  if(question_id != "0"){
    if(question_id){

    selectedBox.append(`<div id=${question_id} class=""><i class="fas fa-arrow-circle-right"></i> ${question_text} <a href='#' class="text-danger" id=${question_id}><i class="fas fa-times"></i></a></div>`);
    $(`#${question_id}`).click(function(){
      $(this).closest('div').remove()
      if(selectedBox.children().length < 1){
        $("#empty_q_box_btn").addClass("disabled");
        $("#continu-btn").addClass("disabled");
      }
    })
    option_selected.remove();
    $("#empty_q_box_btn").removeClass("disabled");
    $("#continu-btn").removeClass("disabled");
  }
    
  }
}

$("#chose-q").on('click', choose_q);

/*----------------//-----------------------------*/
/*--------------------save reuse quiz-----------------*/
function save_reuse(e){
  e.preventDefault();
  $("#exampleModal #close").click();
  var question_tab=[];
  var niveau=$('#reuse_niveau').val();
  var matiere=$('#reuse_matiere').val();
  var description=$('#reuse_description').val();
  var old_quiz=$(".old_quiz").attr("id");
  var motcles=$('#reuse_motcles').val();
  var selectedBox=$('#selected-q-box');
  quest=new FormData()
  //var list_child=selectedBox.children();
  selectedBox.children('div').each(function () {
    question_tab.push($(this).attr("id")); // "this" is the current element in the loop
});
  data=new FormData()
  data.append("reuse_quiz",true);
  data.append("old_quiz", old_quiz);
  data.append("niveau", niveau);
  data.append("matiere",matiere);
  data.append("description",description);
  data.append("motcles",motcles);
  data.append("questionnaire", question_tab);
  data.append(
          "csrfmiddlewaretoken",
          $("input[name=csrfmiddlewaretoken]").val()
        );

  $.ajax({
    type: "POST",
    url:'',
    data:data,
    cache:false,
    processData:false,
    contentType:false,
    success: function(data){
      if(data.success_message){
        notify(data.success_message+"Quiz "+data.quiz_id+"<br/>Vous pouvez maintenant modifier ces questionnaire a vos souhait! <i class='fas fa-smile-beam text-warning'></i>",'success',delay=5000);
        window.setTimeout(function () {
                window.location = `../addquestion/${data.quiz_id}`;
              }, 5000);
      }else{
        notify(data.error_message,'error');
        window.setTimeout(function () {
                window.location = "../";
              }, 2000);
      }
    },
    error: function (error){
      notify("Une erreur s'est produit...",'error');
      window.setTimeout(function () {
                window.location = "../";
              }, 2000);
    },
    async: true,
    timeout: 60000,
  });

}
$("#reuse_form").submit(save_reuse);
/*-----------------//-------------------------------------*/
/*-------------vider le box de question-----------*/

$("#empty_q_box_btn").on('click', function(event){
  event.preventDefault();
  $('#selected-q-box').empty();
  $('#empty_q_box_btn').addClass('disabled');
  $("#continu-btn").addClass("disabled");

})

/*---------------//-------------------------------*/
/*---------------------load matiere--------------*/
function load_matiere(e){
  e.preventDefault();
  var matiere=$('#matiere-field').val();
  var matiereBox=$('#matiere-block');
  if( matiere.length >=2 ){
    matiereBox.text(matiere);
  }
  else{
    alert("Vous devez renseigner une matiere")
  }
}
$('#matiere-btn').on('click', load_matiere);
/*----------//---------------------------------*/

/*---------------------load description--------------*/
function load_description(e){
  e.preventDefault();
  var description=$('#description-field').val();
  var descriptionBox=$('#description-block');
  if( description.length >=5 ){
    descriptionBox.text(description);
  }
  else{
    alert("Description trop courte ou vide...reessayer!")
  }
}
$('#description-btn').on('click', load_description);
/*----------//---------------------------------*/

/*---------------------load mot cles--------------*/
function load_motCles(e){
  e.preventDefault();
  var motcles=$('#motcles-field').val();
  var motclesBox=$('#motcles-block');
  if( motcles.length >=5 ){
    motclesBox.text(motcles);
  }
  else{
    alert("liste de mot cles trop courte ou vide...reessayer!")
  }
}
$('#motcles-btn').on('click', load_motCles);
/*----------//---------------------------------*/

/*------edit quiz request---------------------*/

function save_edit(e){
  e.preventDefault();
  var description=$('#description-block').text();
  var niveau=$('#niveau-block').text();
  var matiere=$('#matiere-block').text();
  var motcles=$('#motcles-block').text();

  data=new FormData()
  data.append('niveau', niveau);
  data.append('matiere', matiere);
  data.append('description', description);
  data.append('motcles', motcles);
  data.append('edit_quiz', true);
  data.append(
          "csrfmiddlewaretoken",
          $("input[name=csrfmiddlewaretoken]").val()
        );
  $.ajax({
    type: "POST",
    url:'',
    data:data,
    cache:false,
    processData:false,
    contentType:false,
    success: function(data){
      if(data.success_message){
        notify(data.success_message,'success');
        window.setTimeout(function () {
                window.location = "../";
              }, 2000);
      }else{
        notify(data.error_message,'error');
        window.setTimeout(function () {
                window.location = "../";
              }, 2000);
      }
    },
    error: function (error){
      notify("Une erreur s'est produit...",'error');
      window.setTimeout(function () {
                window.location = "../";
              }, 2000);
    },
    async: true,
    timeout: 60000,
  })
}
$('#save_edit').on('click',save_edit);

/*---------------//--------------------------*/


$("#mngdelbtn").click(function(e){
  //e.preventDefault();
  $("#manageQuiz #close").click();
});
/*-----delete bouton----------*/
$("#confirmDelete").click(function(e){
  // Extract info from data-bs-* attributes
  var delbtn=document.getElementById('confirmDelete');
  var recipient = delbtn.getAttribute('value');
  var data=new FormData();
  data.append("id_quiz",recipient);
  data.append("del_quiz",true);
  data.append(
          "csrfmiddlewaretoken",
          $("input[name=csrfmiddlewaretoken]").val()
        );

  $.ajax({
    type: "POST",
    url:'',
    data:data,
    cache:false,
    processData:false,
    contentType:false,
    success: function(data){
      if(data.success_message){
        notify(data.success_message,'success');
        alert(data.success_message)
        window.setTimeout(function () {
                window.location = "../";
              }, 2000);
      }else{
        notify(data.error_message,'error');
        alert(data.error_message);
        window.setTimeout(function () {
                window.location = "../";
              }, 2000);
      }
    },
    error: function (error){
      notify("Une erreur s'est produit...",'error');
      window.setTimeout(function () {
                window.location = "../";
              }, 2000);
    },
    async: true,
    timeout: 60000,
  })
  
});
/*--------//----------------*/
/*FONCTION REUTILISABLE======*/
function sendingxmlfile(data){
            if (data.msg != '' && data.msg != 'undefined'){
              notify(data.msg,'success');
              window.setTimeout(function () {
                window.location = "../";
              }, 1000);
            }
            else{
              notify("Votre session a expirer, actualiser la page!","error");
              window.setTimeout(function () {
                window.location = "../";
              }, 2000);
            }
}

function sendingxmlfile2(data){
            if (data.success_message){
              notify(data.success_message,'success');
              window.setTimeout(function () {
                window.location = `./${data.id_quiz}`;
              }, 1000);
            }
            else if (data.error_message){
              notify(data.error_message,"error");
            }
            else{
              notify("Erreur inconue!",'error');
            }
}
/*----------------//---------------------*/


/*la fonction notification permettant l'affichage d'un feedback */
function clear_notify(){
  $("#msg-notify").removeClass("alert-danger");
  $("#msg-notify").removeClass("alert-success");
  $("#msg-notify").removeClass("alert-warning");
  $("#msg-notify").addClass("d-none");

}

function notify(msg,type,delay=2000){

  $("#msg-notify").removeClass("d-none");
  if (type == "error"){

    $("#msg-notify").addClass('alert-danger');
    $("#msg-notify").html('<i class="fas fa-exclamation-triangle"></i>'+msg);

  }
  else if(type == "warning"){
    $("#msg-notify").addClass('alert-warning');
    $("#msg-notify").html('<i class="fas fa-exclamation-triangle"></i>'+msg);
  }
  else{
    $("#msg-notify").addClass('alert-success');
    $("#msg-notify").html('<i class="far fa-check-circle"></i>'+msg);
  }
  setTimeout(function () {
              
    clear_notify();
}, delay);
}
/*----------------//---------------------------------*/


/*Actualise le tableau d'affichage de quiz*/
function add_in_quiz_table(niveau,matiere,id,description,auteur,motcles,date){
  /*ajout de l'item dans le tableau html en creant un tr a chaque fois*/
  $("#table-item").append(`<tr> <th scope="row"> <div class="form-check"><input class="form-check-input" type="checkbox" value="" id="flexCheckDefault"/></div></th>\
      <td>${id}</td>\
      <td>${niveau}</td>\
      <td>${matiere}</td>\
      <td>${description}</td>\
      <td>${motcles}</td>\
      <td>${auteur}</td>\
      <td>${date}</td>\
      <td>\
        <a type="button" href="addquestion/${id}" class="btn waves-effect"><i class="fas fa-upload fa-sm"></i></a>\
      </td>\
      <td>\
        <button value="${id}" id="mngbtn" type="button" class="btn waves-effect" data-bs-toggle="modal" data-bs-target="#manageQuiz" data-bs-whatever=""><i class="fas fa-server"></i></button>\
      </td>\
    </tr>`);

}


function load_quiz_interface(liste_question){
  $("#table-item").empty();
  // Parcourir le tableau et afficher toutes les valeurs
  for(var i = 0; i < liste_question.length; i++){
    var niveau=liste_question[i].niveau;
    var matiere=liste_question[i].matiere;
    var id=liste_question[i].id_quiz;
    var description=liste_question[i].description;
    var auteur=liste_question[i].auteur;
    var motcles=liste_question[i].mot_cles;
    var date=liste_question[i].date;
    add_in_quiz_table(niveau,matiere,id,description,auteur,motcles,date);

  }
}
/*----------------//----------------------------------*/

/* Checking file form------and send data--------------*/
function fileLoad(e){
  e.preventDefault();
  var data=new FormData($('#xml').get(0));
  file_name = $('#formFileSm').val().replace(/C:\\fakepath\\/i, '');

  if (file_name.length <80){
    if (file_name.includes(".xml") == true){
      data.append(
          "csrfmiddlewaretoken",
          $("input[name=csrfmiddlewaretoken]").val()
        );

    $.ajax({
          type: "POST",
          url:$(this).attr('action'),
          data:data,
          cache:false,
          processData:false,
          contentType:false,
          success: function(data){ sendingxmlfile(data); },
          error: function (error) { notify(data.msg,'error');},
          async: true,
          timeout: 60000,
        });
  return false;
  }
  else{
    notify("Veuillez selectioner un fichier .xml Svp!","error");
  }
}else{
  notify("Nom de fichier trop long, vous pouvez raccourcir le nom du fichier en le renommant","error")
 }
}

$(function(){
  $('#xml').submit(fileLoad);
});
/*-----------------------//-------------------------------*/

/*add quiz from form-------------*/
function addFromForm(e){
 e.preventDefault();
  
  var data=new FormData($('#addForm').get(0));
  data.append("add_quiz",true)
  file_name = $('#formFileSm').val().replace(/C:\\fakepath\\/i, '');
  $("#exampleModal #close").click();
  if (file_name.length <80){
    if (file_name.includes(".xml") == true){
      }
  else{
    notify("Veuillez selectioner un fichier .xml Svp!","error");
  }
      data.append(
          "csrfmiddlewaretoken",
          $("input[name=csrfmiddlewaretoken]").val()
        );

    $.ajax({
          type: "POST",
          url:$(this).attr('action'),
          data:data,
          cache:false,
          processData:false,
          contentType:false,
          success: function(data){ sendingxmlfile(data); },
          error: function (error) { notify(data.msg,'error'); alert(data.msg)},
          async: true,
          timeout: 60000,
        });
  return false;
  
}else{
  notify("Nom de fichier trop long, vous pouvez raccourcir le nom du fichier en le renommant","error")
 }

}
$(function(){
  $('#addForm').submit(addFromForm);
});
/*---addquestion interface-------*/
function add_question_Form(e){
 e.preventDefault();
  
  var data=new FormData($('#add_question_Form').get(0));
  data.append("add_quiz",true)
  file_name = $('#formFileSm').val().replace(/C:\\fakepath\\/i, '');
  $("#exampleModal #close").click();
  if (file_name.length <80){
    if (file_name.includes(".xml") == true){
      }
  else{
    notify("Veuillez selectioner un fichier .xml Svp!","error");
  }
      data.append(
          "csrfmiddlewaretoken",
          $("input[name=csrfmiddlewaretoken]").val()
        );

    $.ajax({
          type: "POST",
          url:$(this).attr('action'),
          data:data,
          cache:false,
          processData:false,
          contentType:false,
          success: function(data){ sendingxmlfile2(data); },
          error: function (error) { notify("Une erreur inconnu!",'error');},
          async: true,
          timeout: 60000,
        });
  return false;
  
}else{
  notify("Nom de fichier trop long, vous pouvez raccourcir le nom du fichier en le renommant","error")
 }

}
$(function(){
  $('#add_question_Form').submit(add_question_Form);
});
/*----------//---------------------*/

/*---------------//----------------------------------------*/

/*Filtre par niveau------------------------------------------*/
$('#niveauw').on('change',function(){
  var selected_indice=this.value;
  if(selected_indice != 0){

    data=new FormData()
    data.append('niveau',selected_indice);
    data.append('s-niveau',true);
    data.append(
        "csrfmiddlewaretoken",
        $("input[name=csrfmiddlewaretoken]").val()
      );

    $.ajax({
      type: "POST",
      url: "",
      success: function (data) {
        if (data.success_message) {
          notify(data.success_message,'success');
          load_quiz_interface(data.question_liste);
          }else {
              notify("Aucun quiz trouver pour ce niveau",'error');
              window.setTimeout(function () {
                window.location = "../";
              }, 1000);
            }
          },
      error: function (error) {
            // handle error
          },
          async: true,
          data: data,
          cache: false,
          contentType: false,
          processData: false,
          timeout: 60000,
        });
  }else if(selected_indice == "0"){

      window.setTimeout(function () {
                window.location = "../";
              }, 300);
  }
});
/*------------//----------------------------------------------*/

/*Filtre par matiere------------------------------------------*/
$('#matiere').on('change',function(){
  var selected_indice=this.value;
  /*var niveau=$('.s-niveau[option|="1"]').text();*/

  if(selected_indice != 0){

    data=new FormData()
    data.append('matiere',selected_indice);
    data.append('s-matiere',true);
    data.append(
        "csrfmiddlewaretoken",
        $("input[name=csrfmiddlewaretoken]").val()
      );

    $.ajax({
      type: "POST",
      url: "",

      success: function (data) {
        if (data.success_message) {
          notify(data.success_message,'success');
          /*window.setTimeout(function () {
                window.location = "../";
              }, 500);*/
          
          load_quiz_interface(data.question_liste);
              
            } 
            else {
              notify("Aucun quiz trouver pour cette matiere",'error');
              window.setTimeout(function () {
                window.location = "../";
              }, 1000);
            }
          },
      error: function (error) {
            // handle error
          },

          async: true,
          data: data,
          cache: false,
          contentType: false,
          processData: false,
          timeout: 60000,
        });
  }else if(selected_indice == "0"){

      window.setTimeout(function () {
                window.location = "../";
              }, 300);
  }
  
});
/*-------------------//--------------------------------------*/


/*Filtre par auteur-------------------------------------------*/
$('#auteur').on('change',function(){
  var selected_indice=this.value;
  /*var niveau=$('.s-niveau[option|="1"]').text();*/
  if(selected_indice != 0){

    data=new FormData()
    data.append('auteur',selected_indice);
    data.append('s-auteur',true);
    data.append(
        "csrfmiddlewaretoken",
        $("input[name=csrfmiddlewaretoken]").val()
      );

    $.ajax({
      type: "POST",
      url: "",

      success: function (data) {
        if (data.success_message) {
          notify(data.success_message,'success');
          /*window.setTimeout(function () {
                window.location = "../";
              }, 500);*/
          
          load_quiz_interface(data.question_liste);
              
            } 
            else {
              notify("Aucun quiz trouver pour cet Auteur",'error');
              window.setTimeout(function () {
                window.location = "../";
              }, 1000);
            }
          },
      error: function (error) {
            // handle error
          },

          async: true,
          data: data,
          cache: false,
          contentType: false,
          processData: false,
          timeout: 60000,
        });
  }else if(selected_indice == "0"){

      window.setTimeout(function () {
                window.location = "../";
              }, 300);
  }
  
});
/*----------------//-------------------------------------------*/

/*gestion de recherche par mot cles------------------------*/
function search(e){
  e.preventDefault();
  var word=$("#srch-motcles").val();
  data=new FormData();
  data.append("search",true);
  data.append("word",word);
  data.append("csrfmiddlewaretoken",
          $("input[name=csrfmiddlewaretoken]").val());
  $.ajax({
    type: "POST",
    url:'',
    data:data,
    cache:false,
    processData:false,
    contentType:false,
    success: function (data){
      if(data.success_message){
        notify(data.success_message,'success',delay=5000);
        load_quiz_interface(data.question_liste);
      }
      else if (data.no_resultat_message){
        notify(data.no_resultat_message,'error',delay=5000);
      }
      else{
        notify(data.no_resultat_message,'error',delay=5000);
        window.setTimeout(function () {
                window.location = "../";
              }, 2000);
      }
    },
    error: function(error){
      notify("Desolee , Cette requete n'a pas abouti...reessayer svp",'warning');
      
    }

    });
}
$(function(){
  $("#srch-form").submit(search);
});
/*-----------//-----------------------------------*/


/*Add question liste from xml file--------------------------------*/
function questionLoad(e){

  e.preventDefault();
  var data=new FormData($('#xmlquestion').get(0));
  var quiz_id=$("#id_quiz").value;
 
  file_name = $('#formFileSm').val().replace(/C:\\fakepath\\/i, '');
  if (file_name.length <80){
    if (file_name.includes(".xml") == true){

    data.append(
          "csrfmiddlewaretoken",
          $("input[name=csrfmiddlewaretoken]").val()
        );

    $.ajax({
          type: "POST",
          url:'',
          data:data,
          cache:false,
          processData:false,
          contentType:false,
      success: function (data) {
            if (data.success_message!= '' && data.success_message!= 'undefined'){
              notify(data.success_message,'success');
              window.setTimeout(function () {
                window.location = "../";
              }, 1000);
            }
            else{
              notify(data.error_message,'error');
              notify("Votre session a expirer, actualiser la page!","error");
              window.setTimeout(function () {
                window.location = "../";
              }, 2000);
            }
            
          },
          error: function (error) {
            // handle error
            notify(data.msg,'error');
          },
          async: true,
          timeout: 60000,
        });
    return false;
  }
  else{
    notify("Veuillez selectioner un fichier .xml Svp!","error");
  }
}else{
  notify("Nom de fichier trop long, vous pouvez raccourcir le nom du fichier en le renommant","error")
  }
}

$(function(){
  $('#xmlquestion').submit(questionLoad);
});
/*--------------------//--------------------------------------------------*/


/*Gestion des fenetres modale--------------------------*/
var exampleModal = document.getElementById('exampleModal');
exampleModal.addEventListener('show.bs.modal', function (event) {
  // Button that triggered the modal
  var button = event.relatedTarget
  // Extract info from data-bs-* attributes
  var recipient = button.getAttribute('data-bs-whatever')
  // If necessary, you could initiate an AJAX request here
  // and then do the updating in a callback.
  //
  // Update the modal's content.
  var modalTitle = exampleModal.querySelector('.modal-title')
  var modalBodyInput = exampleModal.querySelector('.modal-body input')

  /*modalTitle.textContent = "Formulaire d'ajout d'un nouveau quiz "+ recipient*/
  /*modalBodyInput.value = recipient*/
});
/*---------------//-----------------------*/


/*---------Gestion du quiz----------------------*/

var exampleModal = document.getElementById('manageQuiz');
exampleModal.addEventListener('show.bs.modal', function (event) {
  // Button that triggered the modal
  var button = event.relatedTarget
  // Extract info from data-bs-* attributes
  var recipient = button.getAttribute('value')
  // If necessary, you could initiate an AJAX request here
  // and then do the updating in a callback.
  //
  // Update the modal's content.
  var modalTitle = exampleModal.querySelector('.modal-title')
  var modalBody = exampleModal.querySelector('.modal-body')
  //modalBody.empty();
  var modalBodyInput = exampleModal.querySelector('.modal-body input')
  var modalDelBtn = exampleModal.querySelector('.modal-body #mngdelbtn')
  var modalEditBtn=exampleModal.querySelector('.modal-body #mngeditbtn')
  var modalShowBtn=exampleModal.querySelector('.modal-body #mngshowbtn')
  modalDelBtn.setAttribute("href",`delete_quiz/${recipient}`)
  modalEditBtn.setAttribute("href",`edit_quiz/${recipient}`)
  modalShowBtn.setAttribute("href",`show_quiz/${recipient}`)

  modalTitle.textContent = "Gestion du quiz "+ recipient
  modalBodyInput.value = recipient
 
});

/*------------//--------------------------------*/

