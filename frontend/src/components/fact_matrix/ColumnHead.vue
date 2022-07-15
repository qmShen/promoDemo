<template>
    <g>
        <line  :y1="0"
               :y2="height" stroke-width="0.5" stroke="red"></line>
        <circle
                :cy="0" :r="5" fill-opacity="1" fill="grey"
                :stroke="stroke" stroke-width="1"
        ></circle>

        <text style="font-size: 10px" transform="translate(0,-10), rotate(-55) ">{{title}}</text>
    </g>
</template>

<script>
import {getFactName} from '@/lib/lib.js'
export default {
    name: "ColumnHead",
    props: ['fact', 'height', 'selectedIdMap'],
    computed:{
        title(){
            return getFactName(this.fact)
        },
        stroke(){
            if(this.selectedIdMap[this.fact.index]){
                return 'red'
            }else{
                return 'none'
            }
        }
    }
}
</script>

<style scoped>

</style>