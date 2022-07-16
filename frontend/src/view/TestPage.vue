<template>
    <div class="main-page" style="height: calc(100vh - 20px);">
        <button @click="clickToInit">Init facts</button>
        <button @click="test">Test</button>
        <button @click="evaluate">generate evaluate</button>
        <Demo v-if="facts" style="width: 100%; height: 100%; " :facts="facts"
              :selectedFactIds="selectedFactIds"
              :candidateFactIds="candidateFactIds"
              :selectedIdMap="selectedIdMap"
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
        selectedIdMap(){
            let map = {}
            this.selectedFactIds.forEach(i=>{
                map[i] = true
            })
            return map
        }
    },
    methods:{
        clickToInit(){

            this.$store.commit('test/updateSelectFactIds', [0,1,2,3,4])
        },
        test(){
            this.$store.commit('test/updateSelectFactIds', [1,2,5,7,9])
            this.$store.dispatch('test/evaluateStory', [1,2,5,7,9]);
        },
        evaluate(){
            let evaluationObjs = []
            for(let rid=0, rLen = this.selectedFactIds.length + 1; rid < rLen; rid++){
                for(let cid = 0, cLen = this.candidateFactIds.length; cid < cLen; cid++){
                    let _selectFactIds = [...this.selectedFactIds]
                    let c = this.candidateFactIds[cid];
                    if(this.selectedIdMap[c] == undefined){
                        _selectFactIds.splice(rid, 0, c)
                        evaluationObjs.push({
                            'rid': rid, 'cid': cid, 'factIds': _selectFactIds
                        })
                    }
                }
            }
            console.log("evaluationObjs", evaluationObjs)
            this.$store.dispatch('test/evaluateStories', evaluationObjs);
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
