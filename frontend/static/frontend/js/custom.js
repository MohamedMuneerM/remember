const addPeople = new Vuex.Store({
  state: {
  	peoples : [{id:-1,name:"test",email:"test@test.com"}],
  	id : 0,
  	modalEdit : [{title:"test", date:"fdgd", message:"fdg",flair:"fdg",medium:"fgdg"}],
  },
  mutations: {
    update (state, name, email) {
      state.name = name
      state.email = email
    },
    incrementId(state){
    	state.id++
    },
    pushLi(state, obj){
    	state.modalEdit.push(obj)
    },
    emptyArray(state){
    	state.modalEdit = []
    }

  }
})


const editModalComp = Vue.component('edit-modal',{
	data : function(){
		return {
			// title : this.$store.state.modalEdit[0].title,
			// date : this.$root.modalEdit.date,
			// message : this.$root.modalEdit.message,
			// flair : this.$root.modalEdit.flair,
			// medium: this.$root.modalEdit.medium,
			// peoples_to_send:[],
			checked : false,
			modalEdit : this.$store.state.modalEdit
		}
	},
	methods : {
		updateEntry : function(){
			const requestOptions = {
		      method: "PATCH",
		      headers: { "Content-Type": "application/json","X-CSRFToken": getCookie("csrftoken") },
		      // credentials: 'include', 
		      body: JSON.stringify(this.modalEdit[0]),
		    };
		    fetch(this.modalEdit[0].url, requestOptions)
		      .then((response) => response.json())
		      .then((data) => {console.log(data); alert("updated successfully")})
		      .catch((error) => {console.log(error); alert("updated Failed")})
			// console.log(this.modalEdit)

		},
	}, 
	template : `
	<div class="modal fade" id="exampleModal" tabindex="-1" role="dialog" aria-labelledby="exampleModalLabel" aria-hidden="true">
	  <div class="modal-dialog modal-dialog-centered" role="document">
	    <div class="modal-content">
	      <div class="modal-header">
	        <h5 class="modal-title" id="exampleModalLabel">Modal title</h5>
	        <button type="button" class="close" data-dismiss="modal" aria-label="Close">
	          <span aria-hidden="true">&times;</span>
	        </button>
	      </div>
	      <div class="modal-body">
	        <form class="table-responsive" >
	          <h3 class="">Edit your Schedule</h3>
	          <div class="form-group">
	            <label for="exampleInputEmadfhdhil1">title</label>
	            <input v-model="modalEdit[0].title" type="text" class="form-control" id="exampleInputEmadfhdhil1" aria-describedby="ssss">
	            <!-- <small id="emailHelp" class="form-text text-muted">We'll never share your email with anyone else.</small> -->

	          </div>
	          <div class="form-group">
	              <label for="datetimepickernew">Date</label>
	              <div class="input-group">
	                  <div class="input-group-prepend">
	                      <span class="input-group-text"><i class="ni ni-calendar-grid-58"></i></span>
	                  </div>
	                  <input v-model="modalEdit[0].date" id="datetimepickernew"  type="text" class="form-control" placeholder="Select date">
	              </div>
	          </div>
	          <div class="form-group">
	            <label for="exampleInputPassword1">Message</label>
	            <textarea  v-model="modalEdit[0].message" rows="5"  class="form-control" id="exampleInputPassword1"></textarea>
	          </div>
	          <div class="form-group">
	            <label for="inputState">Flair</label>
	            <select id="inputState" v-model="modalEdit[0].flair"  class="form-control">
	              <option selected>{{modalEdit[0].flair}}</option>
	              <option >birthday</option>
	              <option >anniversery</option>
	              <option >meeting</option>
	              <option >special day</option>
	              <option >other</option>
	            </select>
	          </div>

	          <div class="form-group">
	            <label for="inputState">Medium</label>
	            <select id="inputState" v-model="modalEdit[0].medium" class="form-control">
	              <option selected>{{ modalEdit[0].medium }}</option>
	              <option>email</option>
	              <option >sms</option>
	              <option >both</option>
	            </select>
	          </div>
	        </form>
	      </div>
	      <div class="modal-footer">
	        <button type="button" class="btn btn-secondary" data-dismiss="modal">Close</button>
	        <button type="button" @click="updateEntry" class="btn btn-primary">Save changes</button>
	      </div>
	    </div>
	  </div>
	</div>


	`
})




const formPeople = Vue.component('more-than-one-form', {
  data: function () {
    return {
    	id : 0,
    	name : "",
    	email : "",
    }
  },
  store : addPeople,
  props: ['value'],
  methods : {
  	returnName : function(){
  		return 'name'+this.$store.state.id
  	},
  	returnEmail : function(){
  		// console.log("changed_email")
  		return 'email'+this.$store.state.id
  	},
  	// updateEntry : function(){
  	// 	console.log("updated")
  	// }
  },
  // mounted : function(){
  // 	this.id++
  // },
  created : function(){
  	this.$store.commit("incrementId")
  	// console.log("created")
  	// console.log(this.$store.state.id)
  	// let aliasName = "name"+this.$store.state.id
  	// let aliasEmail = "email"+this.$store.state.id
  	// console.log(aliasName,aliasEmail)
  	// this.$store.state[aliasName] = ""
  	// this.$store.state[aliasEmail] = ""
  	const obj={
  		id : this.$store.state.id,
  		name : this.name,
  		email : this.email,
  	}
  	this.$store.state.peoples.push(obj)

 	// console.log(this.$store.state.peoples)
 	},
  template: `
  <div>
  	<div class="row" v-bind:id=[this.name]>
		<div class="col-md-6">

		  <label  for="exampleInputPassword1">Name</label>
		  <input v-model="value.name" class="form-control" >
		</div>
		<div class="col-md-6">
		  <label for="exampleInputPassword1">E-Email</label>
		  <input v-model="value.email" class="form-control" id="exampleInputPassword1">
		</div>
	</div> 
  </div>


  `,
})



function getCookie(name) {
    var cookieValue = null;
    if (document.cookie && document.cookie != '') {
        var cookies = document.cookie.split(';');
        for (var i = 0; i < cookies.length; i++) {
            var cookie = cookies[i].trim();
            // Does this cookie string begin with the name we want?
            if (cookie.substring(0, name.length + 1) == (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}




const app = new Vue({
	delimiters: ['[[', ']]'],
	el : "#root",

	components :{formPeople},
	
	data : {
		id : 1,
		hello : "Hello world",
		checked:false,
		title : "",
		date : "",
		message:"",
		flair:"",
		medium:"",
		userDates : [],
		componentKey : 0,

		modalEdit : [],


		credentials: [{name:"",email:""}],
	},
	store : addPeople,
	beforeMount : function list(){
		fetch("/api/")
	      .then((response) => response.json())
	      .then((data) => {
	      	this.userDates.push(data)
	      })
	      .catch((error) => console.log(error))

		// console.log(this.userDates)
	},
	// watch:{
	// 	userDates: function(val, oldVal){
	// 	console.log(`val:${val},old-val:${oldVal}`)
	// 	},
	// },
	methods:{

		editField : async function(url){
			// this.$store.state.modalEdit.splice(0, 1)
			// this.$store.commit("emptyArray")
			// fetch(url)
		 //      .then((response) => response.json())
		 //      .then((data) => {
		 //      	// this.modalEdit.push(data)
		 //      	this.$store.commit("pushLi", data)
		 //      	// this.modalEdit.push(data)
		 //      	console.log(this.$store.state.modalEdit)
		 //      })
		 //      .catch((error) => console.log(error))

		  	const response = await fetch(url);
		  	const json = await response.json();
		  	// const data = await 
		  	// console.log(json)
		  	this.$store.commit("pushLi", json)
		  	this.$store.state.modalEdit.splice(0, 1)
		  // return movies;
			console.log(this.$store.state.modalEdit)
		},


		deleteField:  function(url, idx){
			// console.log(url)
			const requestOptions = {
		      method: "DELETE",
		      headers: { "Content-Type": "application/json","X-CSRFToken": getCookie("csrftoken") },
		      // credentials: 'include', 
		      // body: JSON.stringify(fullArray),
		    };
		    fetch(url, requestOptions)
		      .then((response) => console.log(response))
		      // .then((data) => console.log(data))
		      .catch((error) => console.log(error))

		      // beforeMount()
		      // this.Vue.$forceUpdate();
		      // delete this.userDates[0][idx]
		      // this.userDates.pop();
		      // Object.assign(this.$data,this.$options.data.call(this))
		      // this.$forceUpdate()
		      // console.log(idx)
		      // console.log(this.userDates[0][idx])
		      this.userDates[0].splice(idx, 1)
		      this.componentKey = !this.componentKey
		      // console.log(this.userDates)
		},

		addField: function(){
			// this.fields = this.$store.state.peoples.map((people)=>{
			// 	return people
			// })

			this.credentials.push({name:"", email:""})

			// console.log(this.credentials)

		},
		addEntry: function(e){
			e.preventDefault()

			// print(cred)
			// this.$emit("submitted")
			const fullArray = {
				title : this.title,
				message : this.message,
				date : this.date,
				flair : this.flair,
				medium : this.medium,
				peoples_to_send : this.credentials 
			}

			console.log(this.credentials[0])


			// const requestOptions = {
			// 	method : "POST",
			// 	headers: {"Content-Type": "application/json","X-CSRFToken": getCookie("csrftoken")},
			// 	body: JSON.stringify(fullArray), 

			// }

			// fetch('/api/',requestOptions)
			// 	.then(response => response.json())   
			// 	.then(data => console.log(data))
			// 	.catch(error => console.log(error));

			const requestOptions = {
		      method: "POST",
		      headers: { "Content-Type": "application/json","X-CSRFToken": getCookie("csrftoken") },
		      // credentials: 'include', 
		      body: JSON.stringify(fullArray),
		    };
		    fetch("/api/", requestOptions)
		      .then((response) => response.json())
		      .then((data) => console.log(data))
		      .catch((error) => console.log(error))
		  	 
		  	 

		}
	},

})



