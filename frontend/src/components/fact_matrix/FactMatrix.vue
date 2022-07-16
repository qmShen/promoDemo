<template>
    <svg>
        <circle :cx="width" :cy="height" fill="red" r="20"></circle>
        <g :transform="'translate('+ [mainLeft, mainTop] + ')'">
            <g v-if="yScale">
                <g v-for="(fact, index) in selectFacts" :key="fact.index" :transform="'translate(' + [0, yScale(index)] + ')'">
                    <RowHead :fact="fact" :length="xScale(totalLength - 1)"></RowHead>
                </g>
            </g>
            <g v-if="xScale">
                <g v-for="(fact, index) in candidateFacts" :key="index">
                    <ColumnHead :fact="fact" :height="yScale(factLength - 1)" :transform="'translate(' + [xScale(index), 0] + ')'"
                                :selectedIdMap="selectedIdMap"
                    ></ColumnHead>
                </g>
            </g>
        </g>
    </svg>
</template>

<script>
import * as d3 from 'd3'
import RowHead from "@/components/fact_matrix/RowHead";
import ColumnHead from "@/components/fact_matrix/ColumnHead";
export default {
    name: "FactMatrix",
    components: {ColumnHead, RowHead},
    props:['facts',
        'selectedFactIds',
        'candidateFactIds',
        'selectedIdMap'
    ],
    data(){
        return {
            width: 0,
            height: 0,
            xScale: undefined,
            yScale: undefined,
            unitSize: 20,
            mainLeft: 250,
            mainTop: 200
        }
    },
    mounted(){
        this.width = this.$el.clientWidth;
        this.height = this.$el.clientHeight;
        this.yScale = d3.scaleLinear().domain([0, this.factLength]).range([this.unitSize, this.factLength * this.unitSize])
        this.xScale = d3.scaleLinear().domain([0, this.totalLength]).range([this.unitSize, this.totalLength* this.unitSize])
    },
    watch:{
        factLength(val){
            this.yScale = d3.scaleLinear().domain([0, val]).range([this.unitSize, val*this.unitSize])
        },
        totalLength(val){
            this.xScale = d3.scaleLinear().domain([0, val]).range([this.unitSize, val*this.unitSize])
        }
    },
    methods:{
        calc_all_update_scores(){
        }
    },
    computed:{
        selectFacts(){
            let selectFacts = []
            this.selectedFactIds.forEach(index=>{
                selectFacts.push(this.facts[index])
            })
            return selectFacts
        },
        candidateFacts(){
            let candidateFacts = []
            this.candidateFactIds.forEach(index=>{
                candidateFacts.push(this.facts[index])
            })
            console.log('candidate facts', candidateFacts)
            return candidateFacts
        },
        factLength(){
            return this.selectFacts.length
        },
        totalLength(){
            return this.facts.length
        }
    }
}
</script>

<style scoped>

</style>