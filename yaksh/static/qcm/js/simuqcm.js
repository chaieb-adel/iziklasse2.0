//Code javascript pilotant la simulation du qcm
//**********Non de code WAKANDA-JS*******************

var tatal_question_reussi=0; //total de question deja reussi
var liste_q_reusi=[];//les indice de question resussi
var question_encours=0;
var answer_selected=[];
var is_trueAnswer=false;
var true_answer='';
var multi_answer=[];
var successs=[];
var missed=[];

function refresh_page(){
	window.setTimeout(function () {
                window.location = "";
              }, 100);
}
function close_correct_timers(){
	
	window.setTimeout(function () {
                $('#correction-box').addClass('d-none');
              }, 3000);
}
function make_selection(element){
	var checker=false
		items=document.querySelectorAll('#chx-item');
	for(var i=0; i<items.length;i++){
		if(items[i].getAttribute('style') == "background-color:#4aa3ff;border-color:#4aa3ff"){
			checker=true
		}
	}
	if( checker != true){
		try{
			bg=element.getAttribute('style');
			if(bg == "background-color:#4aa3ff;border-color:#4aa3ff"){
				//deselection
				element.setAttribute('style',"background-color:#eff2f7;border-color:#eff2f7");
				element.setAttribute('cocher',false);
			}else{
				element.setAttribute('style',"background-color:#4aa3ff;border-color:#4aa3ff");
				element.setAttribute('cocher',true);
			}
		}catch{
			//---------
		}
	}
}
function add_to_missed(){
	var current=document.querySelector("#current").textContent;
	console.log("ADDing to missed : "+current)
	var data=new FormData();
	data.append('missed',true);
	data.append('current',current);
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
        //alert(data.success_message)
      }
      else{
        //---------
      }
    },
    error: function (error){
      //-----------
    },
    async: true,
    timeout: 60000,
  });
}

function add_to_success(){
	var current=document.querySelector("#current").textContent;
	console.log("ADDing to success : "+current)
	var data=new FormData();
	data.append('success',true);
	data.append('current',current);
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
        //alert(data.success_message)
      }
      else{
        //---------
      }
    },
    error: function (error){
      //-----------
    },
    async: true,
    timeout: 60000,
  });
}
//check unique reponse
function check_unique(e){
	console.log("choix_unique selected");
	element_selected=e.target;
	make_selection(element_selected);
}

function check_multiple(e){
	element=e.target;
	try{
			bg=element.getAttribute('style');
			if(bg == "background-color:#4aa3ff;border-color:#4aa3ff"){
				//deselection
				element.setAttribute('style',"background-color:#eff2f7;border-color:#eff2f7");
				element.setAttribute('cocher',false)
			}else{
				element.setAttribute('style',"background-color:#4aa3ff;border-color:#4aa3ff");
				element.setAttribute('cocher',true)
			}
		}catch{
			//---------
		}
}
//type of question mulitchoice
try{

var is_multichoice=$("#multichoice-type");
if(is_multichoice.attr("name") == "choix_unique"){
	//on ne peut cocher qu'un seul des items
	Array.from(document.querySelectorAll('#chx-item')).forEach(function(el){
	el.addEventListener('click', check_unique);
	if(el.getAttribute('fraction') == "100"){
		true_answer=el.textContent;}})
	
	}
else if(is_multichoice.attr("name") == "choix_multiple"){
	Array.from(document.querySelectorAll('#chx-item')).forEach(function(el){
	el.addEventListener('click', check_multiple);})
	}
}
catch{
	//-------------
}

//close correction box
$('#close-correct').on('click',function(e){
	$('#correction-box').addClass('d-none');

});

//La correction on click sur bouton valider
$('#ok-reponse').on('click', function(e){
	//createcookie();
	//console.log(readcookie()[0]);
	if(is_multichoice.attr("name") == "choix_multiple" || is_multichoice.attr("name") == "choix_unique"){
	multi_answer=[];
	answer_selected=[];
	var rep='';
	var rep_reussi='';
	var nbr_success=0;
	e.preventDefault();
	$('#correction-box').removeClass('d-none');
	close_correct_timers();
	//parcour des item et ecuperation de ceux cocher et des vrai reponses
	Array.from(document.querySelectorAll('#chx-item')).forEach(function(el){
	if(el.getAttribute("fraction") != "0" ){
		//create true answer array
		multi_answer.push(el.textContent)
		}
	//check if is selected
	if(el.getAttribute("cocher") == "true"){
		answer_selected.push(el.textContent);
		}

	});
	//nous avons la liste des vrai reponse et celui de reponse de l'utilisateur
	//console.log(multi_answer);
	//console.log(answer_selected);
	//parcour des reponse de l'utilisateur et comparer avec ceux vrai
	if(answer_selected.length<multi_answer.length || answer_selected.length>multi_answer.length){
		//l'utilsateur n'a pas cocher toutes les reponse
		$("#stat-correction").addClass('text-danger').html("Echec !");
		$("#icon-correction").addClass('text-danger').html('<i class="fas fa-times-circle fa-5x"></i>');
		add_to_missed();
		for(var i=0; i<multi_answer.length; i++){
			rep+="; "+multi_answer[i];
		}
		$("#les-reponses").html('La (les) réponses etait: <br/>'+rep);
		
	}
	else{
		//les nombre de rep selectionner correspond bien au nombre de vrai reponse , continuons
		rep='';
		rep_trouver=''
		rep_reussi=0;
		//creation de la chaine reponse vrai pour affichage et comptage de bon reponse
		for(var i=0; i<answer_selected.length; i++){
			//cette reponse est dans la liste de bonnes reponses
			if(multi_answer.includes(answer_selected[i])){
				//on a donc un reussi
				rep_reussi+=1;
				//on l'ajoute a la chaine reponse
				rep_trouver+="; "+answer_selected[i];
			}
		}
		//-----------------------------------------------
		//---recupere toute les bonne reponse
		for(var i=0; i<multi_answer.length; i++){
			rep+="; "+multi_answer[i];
		}
		//----------------------------------------
		//correction--------------
		//l'utilisateur a trouver toutes les reponses

		if(rep_reussi == multi_answer.length){
			
			add_to_success();
			$("#icon-correction").removeClass('text-danger');
			$("#icon-correction").addClass('text-success').html('<i class="fas fa-check-circle fa-5x"></i>');
			$("#stat-correction").removeClass('text-danger');
			$("#stat-correction").addClass('text-success').html("Bravooo !");
			$("#les-reponses").html('La (les) réponses etait bien: <br/>'+rep_trouver);
		}
		else{
			//l'utilisatuer a echouer certaines reponse
			add_to_missed();
			$("#icon-correction").removeClass('text-success');
			$("#icon-correction").addClass('text-danger').html('<i class="fas fa-times-circle fa-5x"></i>')
			$("#stat-correction").removeClass('text-success');
			$("#stat-correction").addClass('text-danger').html("Echec !<br/> Vous n'avez pas trouver la bonne réponse; ou alors pas toutes les bonne réponses!");
			$("#les-reponses").html('La (les) réponses etait: <br/>'+rep);
		}
		//---------------------//------------------------------------
	}

}
else if(is_multichoice.attr("name") == "shortanswer"){
	//le short enaswer
	//alert("Short enaswer")
	var re_question=$("#reponse-short").attr("name");
	var reponse_user=$("#reponse-short").val();
	//alert(reponse_user);
	if(reponse_user==re_question){
		//succed
		add_to_success();
		$('#correction-box').removeClass('d-none');
		close_correct_timers()
		$("#icon-correction").removeClass('text-danger');
		$("#icon-correction").addClass('text-success').html('<i class="fas fa-check-circle fa-5x"></i>');
		$("#stat-correction").removeClass('text-danger');
		$("#stat-correction").addClass('text-success').html("Bravooo !");
		$("#les-reponses").html('La réponse etait bien: <br/>'+reponse_user);
	}
	else{
		add_to_missed();
		$('#correction-box').removeClass('d-none');
		close_correct_timers()
		$("#icon-correction").removeClass('text-success');
		$("#icon-correction").addClass('text-danger').html('<i class="fas fa-times-circle fa-5x"></i>')
		$("#stat-correction").removeClass('text-success');
		$("#stat-correction").addClass('text-danger').html("Echec !<br/> Vous n'avez pas trouver la bonne réponse; ou alors pas toutes les bonne réponses!");
		$("#les-reponses").html('La réponses etait: <br/>'+re_question);
	}
}
else if(is_multichoice.attr("name") == "cloze-short"){
	//cloze avec champs de saisi
	var item_cloze=document.querySelectorAll("#chx-item");
	var cloze_rp_liste=[]
	var success_list=0
	
	Array.from(document.querySelectorAll("#chx-item")).forEach(function(element){
		cloze_rp_liste.push(element.getAttribute("name"))
	});
	//console.log(cloze_rp_liste)
	var i=0
	while(i<item_cloze.length){
		if(item_cloze[i].value == cloze_rp_liste[i]){
		success_list+=1;

		}
		
		i=i+1;
	}
	
	if (success_list == cloze_rp_liste.length){
		//---------il a tout reussi
		add_to_success();
		$('#correction-box').removeClass('d-none');
		close_correct_timers()
		$("#icon-correction").removeClass('text-danger');
		$("#icon-correction").addClass('text-success').html('<i class="fas fa-check-circle fa-5x"></i>');
		$("#stat-correction").removeClass('text-danger');
		$("#stat-correction").addClass('text-success').html("Bravooo !");
		$("#les-reponses").html('La réponse etait bien: <br/>'+cloze_rp_liste.join("; "));
	}
	else{
		add_to_missed();
		$('#correction-box').removeClass('d-none');
		close_correct_timers()
		$("#icon-correction").removeClass('text-success');
		$("#icon-correction").addClass('text-danger').html('<i class="fas fa-times-circle fa-5x"></i>')
		$("#stat-correction").removeClass('text-success');
		$("#stat-correction").addClass('text-danger').html("Echec !<br/> Vous n'avez pas trouver la bonne réponse; ou alors pas toutes les bonne réponses!<br/>Vous avez reussi <span style='color:green'> "+success_list+" reponse(s) sur "+cloze_rp_liste.length);
		$("#les-reponses").html('La (les) réponses etait: <br/>'+cloze_rp_liste.join("; "));
	}
	
	}
	else if(is_multichoice.attr("name") == "cloze-select"){
		//close with selection
		
		var rep_true_liste=[];
		var successs_l=0;
		Array.from(document.querySelectorAll("#sel-chx-item")).forEach(function(element){
			if(element.getAttribute("value") == "100"){
				rep_true_liste.push(element.textContent)
			} 
		});
		//recuillir toutes les selects
		Array.from(document.querySelectorAll("#select-cloze")).forEach(function(element){
			if(element.value == "100"){
				successs_l+=1
			}
		});
		//Correction
		if(successs_l == rep_true_liste.length){
			//il a tout reussi
			add_to_success();
			$('#correction-box').removeClass('d-none');
			close_correct_timers()
			$("#icon-correction").removeClass('text-danger');
			$("#icon-correction").addClass('text-success').html('<i class="fas fa-check-circle fa-5x"></i>');
			$("#stat-correction").removeClass('text-danger');
			$("#stat-correction").addClass('text-success').html("Bravooo !");
			$("#les-reponses").html('La réponse etait bien: <br/>'+rep_true_liste.join("; "));
		}
		else{
			//il achouer certains
			add_to_missed();
			$('#correction-box').removeClass('d-none');
			close_correct_timers()
			$("#icon-correction").removeClass('text-success');
			$("#icon-correction").addClass('text-danger').html('<i class="fas fa-times-circle fa-5x"></i>')
			$("#stat-correction").removeClass('text-success');
			$("#stat-correction").addClass('text-danger').html("Echec !<br/> Vous n'avez pas trouver la bonne réponse; ou alors pas toutes les bonne réponses!<br/>Vous avez reussi <span style='color:green'> "+successs_l+" reponse(s) sur "+rep_true_liste.length);
			$("#les-reponses").html('La (les) réponses etait: <br/>'+rep_true_liste.join("; "));
		}
	}
	else if(is_multichoice.attr("name") == "matching_quest"){
		//matching question
		//alert("Matching")
		var match_rep_liste=[];
		var match_success=0;
		var drop_zone_liste=document.querySelectorAll(".example-dropzone")
		Array.from(document.querySelectorAll("#match-rep")).forEach(function(element){
			match_rep_liste.push(element.getAttribute('fraction'));
		})
		for(var i=0; i<drop_zone_liste.length;i++){
			//------
			//les enfants de dropzone pour recuperer l'element depose
			Array.from(drop_zone_liste[i].children).forEach(function(element){
				if(match_rep_liste[i] == element.textContent){
					console.log("Success!!!!!")
					match_success+=1
				}
			})
		}

		if(match_success == match_rep_liste.length){
			add_to_success();
			$('#correction-box').removeClass('d-none');
			close_correct_timers()
			$("#icon-correction").removeClass('text-danger');
			$("#icon-correction").addClass('text-success').html('<i class="fas fa-check-circle fa-5x"></i>');
			$("#stat-correction").removeClass('text-danger');
			$("#stat-correction").addClass('text-success').html("Bravooo !");
			$("#les-reponses").html("Vous avez bien relier les Box de droit a leurs quivalent de gauche");
		}
		else{
			add_to_missed();
			$('#correction-box').removeClass('d-none');
			close_correct_timers()
			$("#icon-correction").removeClass('text-success');
			$("#icon-correction").addClass('text-danger').html('<i class="fas fa-times-circle fa-5x"></i>')
			$("#stat-correction").removeClass('text-success');
			$("#stat-correction").addClass('text-danger').html("Echec !<br/>");
			$("#les-reponses").html("Malheuresement les block ne sont pas bien associer, Resseyez une autre fois.");
		}
	}
});

try{
$('#closemodal').on('click',function(e){
  e.preventDefault();
  $('#exampleModalCenter').modal("hide");
});
}catch{
  //..........
}

try{
$('#retablirBtn').on('click',function(e){
  e.preventDefault();
  $('#exampleModalCenter').modal("hide");
});
}catch{
  //..........
}

function onDragStart(event) {
  event.dataTransfer.setData('text/plain', event.target.id);

  event.currentTarget.style.backgroundColor = 'yellow';
}
var dropped_id_liste=[]
function onDragOver(event) {
  event.preventDefault();
  //event.currentTarget.setAttribute("style","border:1px dashed gray;") 
}

function onDragLeave(event){
	//event.currentTarget.setAttribute("style","border:1px solid gray;")
	var i=0
}

function onDrop(event) {
	event.preventDefault();
  const id = event
    .dataTransfer
    .getData('text');
  /*if(dropped_id_liste.includes(id)){
  	console.log("deja dropper")
  }*/
  if(!(dropped_id_liste.includes(event.target.id))){
  const draggableElement = document.getElementById(id);
  draggableElement.setAttribute('class',"col-md-12 example-draggable bg-dark text-white text-center")
  const dropzone = event.target;
  dropzone.setAttribute("style","font-weight: bold; color:#fff;border:none;min-height: 30px")
  dropzone.appendChild(draggableElement);
  draggableElement.setAttribute('draggable',"false")
  dropped_id_liste.push(id)


}
}

$("#modif_quest").on("click", function(e){
	e.preventDefault();
	alert("La modification de cette question affectera sa visualisation par les eleves. Vous ne devez la modifier qu'en cas d'extreme necessite. La possibilte de modifier une question viendra avec la prochaine version soyez patient. Merci")
})

