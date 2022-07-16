<template>
    <div>
        <fact-matrix style="width: 100%; height: 100%;"
                     :facts="facts"
                     :selectedFactIds="selectedFactIds"
                     :candidateFactIds="candidateFactIds"
                     :selectedIdMap="selectedIdMap"
        ></fact-matrix>
    </div>
</template>

<script>
import FactMatrix from "@/components/fact_matrix/FactMatrix";
export default {
    name: "Demo",
    components: {FactMatrix},
    props: ['facts', 'selectedFactIds', 'candidateFactIds','selectedIdMap']
}
</script>

<style scoped>

</style>