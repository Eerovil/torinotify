var home = Vue.component("home", {
    template: `
    <div>
        <ul>
        <li v-for="entry in entries">
            <a :href="entry.url">{{ entry.name }}</a>, Chat ID: {{ entry.chatId }}
        </li>
        </ul>
        <v-layout ref="layout" row wrap>
            <v-text-field label="URL" v-model="newUrl"></v-text-field>
            <v-text-field label="Name" v-model="newName"></v-text-field>
            <v-text-field label="ChatId" v-model="newChatId"></v-text-field>
            <v-btn @click="addEntry">Add</v-btn>
        </v-layout>
    </div>
    `,
    data() {
        return {
            newUrl: "",
            newName: "",
            newChatId: "",
        }
    },
    computed: {
        entries() {
            return this.$store.state.entries;
        },
    },
    methods: {
        addEntry() {
            axios.post("addentry", {url: this.newUrl, chatId: this.newChatId, name: this.newName}).then(response => {
                console.log(response)
                this.$store.commit('updateEntries', response.data.entries);
            })
        }
    },
    mounted() {
        axios.get("fetchentries").then(response => {
            console.log(response)
            this.$store.commit('updateEntries', response.data.entries);
        })
    }
});