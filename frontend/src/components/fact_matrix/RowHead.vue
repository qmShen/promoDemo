<template>
    <g>
        <circle :cy="0" :cx="0" :r="5" fill-opacity="0.5"></circle>
        <text style="font-size: 10px; " :x="-textLength" :y="textHeight / 2">
            {{title}}
        </text>
        <line :x1="0" :x2="length" :y1="0" :y2="0" stroke-width="0.5" stroke="red"></line>
    </g>
</template>

<script>
import * as d3 from 'd3'
import {getFactName} from '@/lib/lib.js'
export default {
    name: "RowHead",
    props: ['fact', 'length'],
    data(){
        return {
            textLength: 0,
            textHeight: 0
        }
    },
    mounted(){
        let box = d3.select(this.$el).select('text').node().getBBox()
        this.textLength = box.width + 10;
        this.textHeight = box.height;
    },
    computed:{
        title(){
            return getFactName(this.fact)
        }
    }
}
</script>

<style scoped>

</style>