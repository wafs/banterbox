<template>


    <div v-if="!room.found && !room.loading">
        <h5 style="color:red;background-color: black;padding:30px;">Oh noes! Database Sez : no available rooms for this
            unit. </h5>
    </div>
    <div class="row" v-if="store.units.units.length > 0">


        <!--<div v-if="!room.loading && room.authorized">-->

        <!--<h5>-->
        <!--If you are seeing this, the room's data has not loaded or auth fail, or some other crap.-->
        <!--Check console and see if something shit itself-->
        <!--</h5>-->
        <!--</div>-->

        <div v-if="!room.loading && !room.authorized">
            <h5>You have been blacklisted from this room :(</h5>
            <h5>Sorry sweaty~</h5>
        </div>
    </div>

    <div id="modal" v-if="modal" transition="fade">
        <div id="modal-content">
            <div autocomplete="off">
                <div class="container">
                    <h2>Edit Settings</h2>

                    <div class="form-group row">
                        <label class="col-xs-3 col-form-label">Icon</label>
                        <div class="col-xs-2" id="icon-preview-container"><i
                                class="fa fa-4x fa-{{settings.unit_icon}}"></i></div>
                        <div class="col-xs-7">

                            <div id="settings-icon-container">
                                <i v-for="icon in settings.icons"
                                   class="fa fa-2x fa-{{icon}} {{icon === settings.unit_icon ? 'selected' : ''}}"
                                   :title="icon"
                                   @click="setIcon(icon)"
                                ></i>
                            </div>
                        </div>
                    </div>

                    <div class="form-group row">
                        <label for="description" class="col-xs-3 col-form-label">Unit Name</label>
                        <div class="col-xs-9">
                            <input type="text" v-model="settings.unit_name" class="form-control" id="description"
                                   name="description">
                        </div>
                    </div>


                    <div class="form-group row">
                        <label class="col-xs-3 col-form-label">Password Protected</label>
                        <div class="col-xs-9">
                            <!-- Radio Buttons -->
                            <label class="form-check-inline">
                                <input class="form-check-input" type="radio" v-model="settings.password_protected"
                                       :value="true">
                                Yes
                            </label>
                            <label class="form-check-inline">
                                <input class="form-check-input" type="radio" v-model="settings.password_protected"
                                       :value="false"
                                       checked> No
                            </label>
                        </div>
                    </div>

                    <div class="form-group row">
                        <label class="col-xs-3 col-form-label">Password</label>
                        <div class="col-xs-9">
                            <input type="text" class="form-control" v-model="settings.password"
                                   :disabled="!settings.password_protected">
                        </div>
                    </div>

                    <div class="form-group row" id="blacklist-row">
                        <label class="col-xs-3 col-form-label">Blacklist</label>
                        <div class="col-xs-9">
                            <div class="row">
                                <div class="col-xs-5">
                                    <label>Allowed</label>
                                    <select multiple class="form-control" id="allowed-users">
                                        <option v-for="user in settings.users" v-if="!user.blacklisted"
                                                :value="user.id">
                                            {{ user.username }}
                                        </option>
                                    </select>
                                </div>
                                <div class="col-xs-2" id="blacklist-controls">
                                    <button class="btn btn-sm" @click.prevent()="setUsersBlacklisted()"> >></button>
                                    <button class="btn btn-sm" @click.prevent()="setUsersAllowed()"> <<</button>
                                </div>
                                <div class="col-xs-5">
                                    <label>Blacklisted</label>
                                    <select multiple class="form-control" id="blacklisted-users">
                                        <option v-for="user in settings.users" v-if="user.blacklisted"
                                                :value="user.id">
                                            {{ user.username }}
                                        </option>
                                    </select>
                                </div>
                            </div>
                        </div>
                    </div>


                    <div class="form-group row">
                        <div class="offset-xs-3 col-xs-9">
                            <button type="submit" class="btn btn-success" @click.prevent="submitSettingsForm()">
                                Submit
                            </button>
                            <button type="submit" class="btn btn-danger" @click.prevent="closeModal()"
                                    style="margin-left: 20px;">Cancel
                            </button>
                        </div>
                    </div>
                </div>
            </div>
        </div>
    </div>


    <div class="col-xs-12" v-show="!room.loading && room.found">
        <div class="col-xs-12">
            <div>
                <h1><i class="unit-icon fa  fa-{{ unit_icon }}"> </i> {{ unit_code }}
                    <button @click="openModal()" v-if="room.role === 'owner'"
                            class="settings-button btn btn-danger btn-sm"><i class="fa fa-cog"></i>Room Settings
                    </button>

                    <button v-link="{ path : '/units/' + unit_code + '/analytics' }" v-if="room.role === 'owner'"
                            class="settings-button btn btn-danger btn-sm"><i class="fa fa-line-chart"></i>
                        Unit Analytics
                    </button>


                </h1>
                <h5>Status : {{ room.status }}</h5>
                <div v-if="room.role === 'owner'">
                    <button class="btn btn-danger" @click="toggleParty" v-if="party_mode">Stop the party :(</button>
                    <button class="btn btn-danger" @click="toggleParty" v-if="!party_mode">Start the party :)</button>
                </div>
            </div>
            <div style="color:dimgray;"><h3 style="font-weight: 200;">{{ unit_name }}</h3></div>
        </div>

        <div class="col-xs-12" style="margin-bottom:20px; position: relative" id="canvas-containers">


            <canvas v-show="!mute_background" id="fg_canvas"
                    style="width:100%; position: absolute; top: 0; left: 0; height:350px; z-index: 2">

            </canvas>
            <canvas v-show="!mute_background" id="bg_canvas" :class="{party : party_mode}"
                    style="width:100%; position: absolute; top: 0; left: 0; height:350px; z-index: 1; background-color: darkslategray">

            </canvas>

            <!-- This div is a dud to stop the parent from collapsing -->
            <div id="dud" style="width:100%; height:350px;"></div>

            <div id="worm-comments">

            </div>
        </div>


        <div class="col-xs-12">
            <div class="row">
                <div class="col-xs-12">
                    <form @submit.prevent="submitComment()" id="comments-form">
                        <input type="text" v-model="comment"
                               :placeholder="room.status == 'running' ? Add a comment : 'You may only post a comment to a running room.'"
                               :disabled="!socket || room.status != 'running'">
                        <button class="btn btn-primary" :disabled="!socket || room.status != 'running'">SUBMIT</button>
                    </form>
                </div>
                <div class="col-xs-4">
                    <div class="text-xs-center">
                        <span class="vote-icon-container" id="upvote">
                            <i @click="changeVote('yes')" class="vote-icon fa fa-5x fa-thumbs-o-up"
                               :class="{green : vote_direction === 'yes'}"></i>
                        </span>
                    </div>
                    <div class="text-xs-center">
                        <span class="vote-icon-container" id="downvote">
                            <i @click="changeVote('no')" class="vote-icon fa fa-5x fa-thumbs-o-down"
                               :class="{red: vote_direction === 'no'}"></i>
                        </span>
                    </div>
                </div>
                <div class="col-xs-8">

                    <div id="comments-panel">
                        <div v-if="!socket">
                            Not connected to server
                        </div>

                        <div class="comment" :id="comment.id" v-for="comment in comments" track-by="$index">
                            <div>
                                <span class="comment-hash"><i class="fa fa-{{comment.icon}}">  </i>  @{{ comment.author }}</span>
                                <span class="comment-time">{{comment.date}} - {{comment.time}}</span>
                                <div class="comment-text">{{ comment.content }}</div>
                            </div>
                            <div @click="kickUser(comment.author)" v-if="(room.role === 'moderator' || room.role == 'owner')">
                                <i class="fa fa-gavel"> </i>
                            </div>
                        </div>

                    </div>
                </div>
            </div>
        </div>
    </div>
</template>


<style lang="scss" rel="stylesheet/scss">
    @import "../../../sass/colours";

    #icon-preview-container {
        justify-content: center;
        display: flex;
        align-items: center;
    }

    #settings-icon-container {
        display: flex;
        width: 100%;
        height: 195px;
        overflow: auto;
        flex-wrap: wrap;
        justify-content: flex-start;
        align-items: flex-start;
        border-radius: 3px;
        border: 1px solid gainsboro;

        i {
            padding: 5px;
            margin: 3px;
            width: 50px;
            display: flex;
            height: 50px;
            border: 1px solid gainsboro;
            justify-content: center;
            align-items: center;
            color: #464646;
            transition: all 0.15s ease-out;

            &:hover {
                transform: scale(1.1)
            }

            &.selected {
                box-shadow: 0px 4px 6px -2px rgba(0, 0, 0, 0.67);
                color: gainsboro;
                background-color: #464646;
                transform: scale(1.2);
            }
        }
    }

    #blacklist-controls {
        display: flex;
        justify-content: center;
        align-items: center;
        flex-direction: column;

        button {
            font-weight: bold;
            color: white;
            margin: 10px 0;
            background-color: $header-background;
        }
    }

    *:disabled {
        cursor: not-allowed;
    }

    #blacklist-row {
        select {
            overflow-y: scroll;
            height: 250px;
        }
    }

    #modal {
        width: 100%;
        height: 100%;
        position: fixed;
        background-color: rgba(0, 0, 0, 0.6);
        top: 0;
        left: 0;
        z-index: 1000000;
        display: flex;
        justify-content: center;
        align-items: center;

        #modal-content {
            overflow: auto;
            padding: 10px;
            width: 80%;
            max-height: 90%;
            background-color: white;
            border-radius: 3px;
            box-shadow: 0 7px 8px -3px rgba(0, 0, 0, 0.78);
        }
    }

    .settings-button {
        i {
            padding-right: 5px;
        }

        margin-left: 10px;;
    }

    #comments-form {

        display: flex;
        margin-bottom: 10px;
        input {
            padding: 3px 3px 3px 10px;
            flex: 1;
            margin-right: 10px;
        }

        .btn {
            background-color: $header-background;
        }
    }

    .vote-icon-container {
        display: flex;
        justify-content: center;
        align-items: center;

        .vote-icon {
            display: flex;
            justify-content: center;
            align-items: center;
            padding: 20px;
            border-radius: 1000px;
            width: 100px;
            height: 100px;
            border: 2px solid #b4b4b4;
            margin: 10px;

            transition: all 0.25s ease;

            box-shadow: 0px 2px 0 0 #3b3b3b;

            &:hover {
                box-shadow: 0px 6px 0 0 #3b3b3b;
                transform: translateY(-3px);
            }

            &.red {
                background-color: red;
                border: 2px solid transparent;
            }

            &.green {
                background-color: #23cd23;
                border: 2px solid transparent;
            }

        }
    }

    #comments-panel {
        border: 3px dashed rgba(122, 122, 122, 0.25);
        max-height: 250px;
        overflow-x: hidden;
        overflow-y: scroll;

        .comment {
            display: flex;
            justify-content: space-between;
            align-items: center;
            background-color: white;
            padding: 5px;
            margin-bottom: 5px;
            border-radius: 2px;
            margin-right: 3px;

            .fa-gavel {
                padding: 10px;
                font-size: 1.5em;
                color:#b8b8b8;

                transition:all 0.25s ease;

                &:hover{
                    color:black;
                    transform:scale(1.1,1.1);
                }
            }

            .comment-username {
                font-weight: 600;
            }

            .comment-time {
                font-size: 0.7rem;
            }

            .comment-text {
                padding: 5px;
                font-size: 0.95rem;
            }
        }
    }


    #canvas-containers{
        perspective: 700px;
    }


    #bg_canvas{
        transition: all 0.25s ease;

        &.party{
            transform: rotateX(55deg) translateZ(-50px)
        }
    }

</style>


<script>
    import auth from '../auth'
    import {store} from '../store'
    import moment from 'moment'
    import io from 'socket.io-client'
    import swal from 'sweetalert2'
    export default {
        data: () => {
            return {
                store,
                party_mode: false,
                settings: {
                    unit_name: null,
                    unit_icon: null,
                    password_protected: false,
                    password: null,
                    users: [],
                    icons: []

                },
                socket: null,
                canvas_running: false,
                worm: null,
                comment: '',
                comments: [],
                vote_direction: 0,
                unit_code: null,
                unit_icon: null,
                unit_name: null,
                modal: false,
                room: {
                    authorized: true,
                    id: null,
                    loading: true,
                    role: null,
                    status: null,
                    found: false
                }
            }
        },
        methods: {


            kickUser(name){
                const role = this.room.role
              if(role === 'moderator' || role === 'owner'){
                  swal({
                        title: `Kick ${name}?`,
                        type: 'success',
                        confirmButtonColor: '#17b000',
                        showCancelButton: true,
                          showCloseButton: true,

                        cancelButtonColor: '#d33',
                        confirmButtonText: 'OK'
                    }).then(() => {
                      this.socket.emit('kick_user', name)
                  }).catch(err => {
                      console.log({err})
                  })
              }
            },

            toggleParty(){
                if (this.room.role === 'owner') {

                    if (!this.party_mode) {
                        this.socket.emit('party_start')
                    } else {

                        this.socket.emit('party_stop')
                        this.party_mode = false
                    }
                }
            },

            /**
             * Send updated settings to the server
             */
            submitSettingsForm(){

                const blacklist = [];
                const whitelist = []

                // Set up the people who are to be blacklisted/removed from blacklist
                this.settings.users.forEach(x => {
                    if (x.blacklisted) {
                        blacklist.push(x.id)
                    } else {
                        whitelist.push(x.id)
                    }
                })


                // Send the request, and on return - adjust values of the room data.
                this.$http.put(`/api/room/${this.room.id}/settings`, {
                    unit_name: this.settings.unit_name,
                    unit_icon: this.settings.unit_icon,
                    password_protected: this.settings.password_protected,
                    password: this.settings.password,
                    blacklist,
                    whitelist
                }).then(() => {
                    this.unit_icon = this.settings.unit_icon
                    this.unit_name = this.settings.unit_name
                    const global_unit = this.store.units.units.find(x => x.code === this.unit_code)
                    global_unit && (global_unit.icon = this.unit_icon)
                }).then(() => {
                    this.closeModal()
                }).then(() => {
                    swal({
                        title: 'Saved!',
                        text: 'Your settings have been udpated',
                        type: 'success',
                        confirmButtonColor: '#17b000',
                        cancelButtonColor: '#d33',
                        confirmButtonText: 'OK'
                    })
                }).catch(error => console.log({error}))
            },


            /**
             * Choose the icon in the settings page.
             */
            setIcon(icon){
                this.settings.unit_icon = icon
            },

            /**
             * Change selected users to blacklisted on the settings page
             */
            setUsersBlacklisted(){
                [...document.getElementById('allowed-users').options]
                        .forEach(x => {
                            if (x.selected) {
                                this.settings.users.find(u => u.id == x.value).blacklisted = true
                            }
                        })
            },

            /**
             * Change selected users to allowed on the settings page
             */
            setUsersAllowed(){
                [...document.getElementById('blacklisted-users').options]
                        .forEach(x => {
                            if (x.selected) {
                                this.settings.users.find(u => u.id == x.value).blacklisted = false
                            }
                        })
            },

            /**
             * Open the settings modal.
             * Before opening it will fetch the settings data from the server and set it up.
             */
            openModal(){
                this.$http.get(`/api/room/${this.room.id}/settings`)
                        .then(response => {
                            console.log({response})

                            this.settings.users = [...response.data.enrolled]
                            this.settings.unit_icon = response.data.icon
                            this.settings.unit_name = response.data.unit_name
                            this.settings.password_protected = response.data.password_protected
                            this.settings.password = response.data.password
                            this.settings.icons = [...response.data.icons]


                            this.modal = true
                        })
            },

            /**
             * Closes the modal and cleans up after itself.
             */
            closeModal(){
                this.modal = false
                Object.assign(this.settings, {
                    unit_name: null,
                    unit_icon: null,
                    password_protected: false,
                    password: null,
                    users: [],
                    icons: []
                })
            },

            /**
             * Submits a comment
             */
            submitComment(){
                if (this.comment.trim().length > 0) {
                    this.socket.emit('comment', {comment: this.comment})
                    this.comment = ''
                }
            },


            /**
             * Initialises a socket and attempts to authenticate.
             *
             * If the socket authenticates, it then proceeds to add all the listeners required to communicate
             * with the room.
             *
             * Otherwise it will just fail.
             *
             */
            initSocket(){
                const socket = io(`//${window.location.hostname}:3000`);


                socket.on('unauthorized', function (err) {
                    console.log("There was an error with the authentication:", err.message);
                })

                socket.on('connect', () => {
                    console.log({room: this.room, id: this.room.id})
                socket.on('authenticated', (e) => {
                    console.log('authenticated')


                this.worm = new Worm(document.getElementById('fg_canvas'), document.getElementById('bg_canvas'), socket)

                // Backlog of comments for the room
                socket.on('comment_history', comments => {
                    this.comments = [...comments]
            })

                // Any time a comment is received
                socket.on('comment', comment => {
                    console.log({comment})
                this.comments.unshift(comment)
            })

                // Any time a server-side message is received
                socket.on('message', data => {
                    console.log({data})
            })

                socket.on('kicked', data => {
                    store.alerts.addAlert({type: 'danger', message: 'You have been removed from the room.'})
                this.$router.go('/units')
            })

                socket.on('blacklisted', data => {
                    store.alerts.addAlert({
                    type: 'danger',
                    message: 'You have been blacklisted from this unit.'
                })
                this.$router.go('/units')

            })

                socket.on('party_start', () => {
                    store.alerts.addAlert({type: 'info', message: 'Oooo yeah... party mode activated'})
                this.worm.set_style({party: true})
                    this.party_mode = true
            })

                socket.on('party_stop', () => {
                    store.alerts.addAlert({
                    type: 'info',
                    message: "If you can't handle me at my memeiest, you definitely can't handle me at my creamiest."
                })
                    this.party_mode = false
                this.worm.set_style({party: false})
            })

                this.socket = socket;
            })

                socket.emit('authentication', {token_id: auth.getToken(), room_id: this.room.id});

            })
        },


            /**
             * Sets the value of the user's current vote.
             * If they click the same button it will cancel their vote and they will be in a neutral state
             * @param value
             */
            changeVote(value){
                if (this.vote_direction === value) {
                    this.vote_direction = 'cancel'
                } else {
                    this.vote_direction = value
                }

                this.socket.emit('vote', {value: this.vote_direction, timestamp: Date.now()})
            }
        },
        route: {
            /**
             * On route activation, collect page data to load the room and activate the worm.
             * If they are unauthorized, nothing will be loaded.
             */
            activate() {

                const room_id = this.$route.query.room_id
                const query_string = room_id ? `?room_id=${room_id}` : ''

                this.$http.get(`/api/unit/${this.$route.params.id}${query_string}`)
                        .then(response => {
                            this.room.found = true
                            this.room.id = response.data.room_id
                            this.unit_code = response.data.unit_code
                            this.unit_icon = response.data.unit_icon
                            this.unit_name = response.data.unit_name
                            this.room.role = response.data.role
                            this.room.loading = false
                            this.room.found = true
                            this.room.status = response.data.room_status
                            console.log(response)

                            this.initSocket()

                            this.canvas_running = true
                            console.log('starting canvas')

                        }, error => {

                            this.room.loading = false

                            if (error.status === 404) {
                                this.room.found = false
                            } else if (error.status === 403) {

                                // user forbidden
                                this.room.authorized = false
                            }
                            console.log({error})
                        })


            },

            /**
             * On page leave, clean up running objects
             */
            deactivate () {

                this.canvas_running = false
                this.worm = null
//                this.socket.emit('leave_room', this.room.id)
                this.socket && this.socket.close()
                this.socket = null
                console.log('stopping canvas')
            }
        },

        /**
         * After the page has loaded, init the socket.
         */
        ready(){
        }
    }
</script>