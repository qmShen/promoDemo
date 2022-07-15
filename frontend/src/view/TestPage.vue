<template>
    <div class="main-page" style="height: calc(100vh - 20px);">
        <button @click="clickToInit">Init facts</button>
        <button @click="test">Test</button>
        <button @click="evaluate">generate evaluate</button>
        <Demo v-if="facts" style="width: 100%; height: 100%; " :facts="facts"
              :selectedFactIds="selectedFactIds"
              :candidateFactIds="candidateFactIds"
        ></Demo>
    </div>
</template>

<script>
// import TestComponent from "@/components/test-page/TestComponent";
import {mapState} from "vuex";
import Demo from "@/components/Demo";
import * as d3 from 'd3'

export default {
    name: 'TestPage',
    components: {
        Demo
        // TestComponent,
    },
    data(){
        return {
            facts: undefined
        }
    },
    mounted(){
        this.$store.dispatch('test/fetchData');
    },
    computed: {
        ...mapState('test', {
            promoFacts: state => state.promoFacts,
            selectedFactIds: state => state.selectedFactIds,
            candidateFactIds: state => state.candidateFactIds,
        }),
    },
    methods:{
        clickToInit(){

            this.$store.commit('test/updateSelectFactIds', [0,1,2,3,4,5,6,7,8,9,10])
        },
        test(){
            this.$store.commit('test/updateSelectFactIds', [1,2,5,7,9])
            this.$store.dispatch('test/evaluateStory', [1,2,5,7,9]);
        },
        evaluate(){
            for(let i=0, ilen=this.candidateFactIds.length; i < ilen+1; i++){
                console.log(i)
            }
        }
    },
    watch:{
        promoFacts(newVal){
            if(newVal){
                this.facts = d3.filter(newVal, record=>record['measure'] == 'PTS')
                this.facts.forEach((fact, i)=>{
                    fact.index = i
                })
            }
        }
    }
}
</script>

<style >
.boundary {
    /*border-style: dashed;*/
    border-style: solid;
    border-color: #d3dce6;
    border-width: 0.5px;
    border-radius: 3px;
}

</style>
