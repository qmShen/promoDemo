import pandas as pd

def get_relation_type(s1, s2):
    sbs_list1 = s1.split('_') if type(s1) is str else s1
    sbs_list2 = s2.split('_') if type(s2) is str else s2
    assert len(sbs_list1) == len(sbs_list2)
    length = len(sbs_list1)
    larger = False
    compare_results = [2 if sbs_list1[i] == sbs_list2[i] #左右相等
                       else 3 if sbs_list1[i] == '*' and sbs_list2[i] != '*'  # 左边是右边的parants
                       else 0 if sbs_list1[i] != '*' and sbs_list2[i] == '*' # 右边是左边的parants
                       else 1 if (sbs_list1[i] != sbs_list2[i]) and (sbs_list1[i] != '*' and sbs_list2[i] != '*')
                       else -1
                       for i in range(0, length)]

    if compare_results.count(3) == 1 and compare_results.count(2) == length-1:
        return '>', compare_results.index(3)
    elif compare_results.count(0) == 1 and compare_results.count(2) == length-1:
        return '<', compare_results.index(0)
    elif compare_results.count(2) == len(sbs_list1):
        return 'same', None
    elif compare_results.count(1) == 1 and compare_results.count(2) == length-1:
        if compare_results[0] == 1:
            return 'temporal', compare_results.index(1)
        else:
            return 'brothers', compare_results.index(1)
    return None, None

class StoryEvaluator:
    def __init__(self, df=None, story_list=None):
        self.promo_df = None
        self.story_list = []
        if df is not None and story_list is not None:
            self.set_df_and_story_list(df, story_list)

    def set_df_and_story_list(self, df, story_list):
        self.promo_df = df
        relative_scores = []
        min_score = min(self.promo_df['total score'])
        max_score = max(self.promo_df['total score'])
        for i in range(0, self.promo_df.shape[0]):
            fact = self.promo_df.iloc[i]
            total_score = fact['total score']
            relative_score = self.promo_df[self.promo_df['total score'] <= total_score].shape[0] / self.promo_df.shape[
                0]
            relative_scores.append(relative_score)
        self.promo_df['relative_score'] = relative_scores
        ## TODO: hard code
        self.promo_df = self.promo_df[self.promo_df['measure'] == 'PTS']
        self.promo_df.loc[:,'id'] = self.promo_df.index
        self.promo_df.loc[:,'subs_list'] = self.promo_df['subspace'].apply(lambda subspace: subspace.split('_'))
        attributes = ['year', 'age', 'team_name', 'lg_name', 'pos_name']
        self.promo_df.loc[:,attributes] = self.promo_df['subs_list'].to_list()



        self.story_list = story_list
        self.story_facts = self.promo_df.iloc[self.story_list]

    def set_story_list(self, story_list):
        self.story_list = story_list
        self.story_facts = self.promo_df.iloc[self.story_list]

    def calc_promotiveness(self):
        ## (1)
        return self.story_facts['relative_score'].sum() / self.story_facts.shape[0]

    def calc_tension_score(self):
        ## (2)
        return 0

    def calc_connection_score(self):
        # (3)
        def relation_scoring(fact1, fact2):
            relation_type = get_relation_type(fact1['subs_list'], fact2['subs_list'])
            if relation_type[0] in ['temporal']:
                return 1
            elif relation_type[0] == 'brothers':
                return 0.8
            elif relation_type[0] == '>':
                return 0.3
            return 0

        relation_score = 0

        for i in range(0, len(self.story_facts) - 1):
            relation_score += relation_scoring(self.story_facts.iloc[i], self.story_facts.iloc[i + 1])
        return relation_score / (1 * (self.story_facts.shape[0] - 1))

    def calc_uniformity(self):
        # (4)
        n_diff = 0
        pre_index = -1
        for i in range(0, len(self.story_list) - 1):
            fact1 = self.promo_df.iloc[i]
            fact2 = self.promo_df.iloc[i + 1]
            (t, current_index) = get_relation_type(fact1['subs_list'], fact2['subs_list'])
            if pre_index == -1:
                pre_index = current_index
            else:
                if current_index is None:
                    n_diff += 1
                elif pre_index != current_index:
                    n_diff += 1
            pre_index = current_index
        return n_diff / (len(self.story_list) - 1)

    def calc_coverage(self):
        # (5)
        return self.story_facts.shape[0] / self.promo_df.shape[0]

    def calc_length_score(self):
        # (6)
        return 0

    def calc_score(self):
        return {
            'promotiveness': self.calc_promotiveness(),
            'tension': self.calc_tension_score(),
            'connection': self.calc_connection_score(),
            'uniformity': self.calc_uniformity(),
            'coverage': self.calc_coverage(),
            'length': self.calc_length_score()
        }

if __name__ == '__main__':
    promo_df = pd.read_csv('./data/NBA_K.csv')
    story_list = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9]
    evaluator = StoryEvaluator(df = promo_df, story_list=story_list)
    print(evaluator.calc_score())