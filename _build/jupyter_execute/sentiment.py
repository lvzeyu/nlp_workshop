#!/usr/bin/env python
# coding: utf-8

# # Transformersによるセンチメント分析

# ## イントロ
# 
# ### はじめに
# 
# 自然言語処理（NLP: Natural Language Processing）は、人間が日常的に使っている自然言語をコンピュータに処理させる一連の技術であり、人工知能（AI）の研究分野で中核を成す要素技術の一つといえます。
# 
# 私たちは普段、自分たちの言語の複雑さについて考えることはありません。言語は歩くのと同じように、訓練された反復可能な行動であるため、習得しやすく、青年期にはより自然に使用できるようになると言われています。ただ、人間にとって自然なことでも、大量の非構造化データを処理し、正式なルールがないばかりか、現実世界のコンテキストや意図もないコンピューターにとっては、それを成すことは非常に困難です。
# 
# 近年、自然言語処理技術の急速な進歩に驚きの声が上がっていました。
# 
# 実際、自然言語処理において昨今の支配的な手法は、隠れマルコフモデル(HMM)、線型サポートベクトルマシン(SVM)やロジスティック回帰など統計的機械学習(statistical machine learning)に基づいていました。
# 
# 2014年頃、この分野において、非線型ニューラルネットワークが導入され、多くのタスクにより高い性能を達成できました。これに基づいて、より先進的なモデリング方法の開発も進めました。特に、再帰的ニューラルネットワーク(RNN)に基づく方法は言語の時系列性質も学習できるになって、様々なタスクにおいて精度向上に大きく貢献しました。
# 
# 2018年にGoogleが発表した「BERT」というシステムでは、開発者が少し手を加えるだけでさまざまなタスクに使えるようになりました。それだけでも驚きでしたが、一般人の中でも話題になる「ChatGPT」をはじめとする自然言語処理技術の進展により、質問への回答、文章の要約や翻訳、ソフトウエアのプログラミングなど、言語に関わるさまざまなタスクができるようになりました。
# 
# 高機能化のカギは、深層学習技術の発展があります。深層学習を用いた自然言語処理には、あらかじめ用意した膨大な文章を使って、「言語モデル」と呼ばれるシステムを学習させる方法があります。
# 言語モデルの実体は簡単な計算式を大量に組み合わせた超巨大な数式といえます。最先端の言語モデルでは、想像を絶するほど大量の文章を使い、パラメータ（数式の係数）が数千億に達するほどの大規模な言語モデル(LLM : Large Language Models)を学習させて使っています。LLMが人間に匹敵するほどの高度な能力を持つ、文章の作成や会話を利用するさまざまな仕事を、コンピュータに任せることが可能になってきました。
# 
# ### テキスト分類
# 
# テキスト分類とは、事前定義済みカテゴリまたはラベルを非構造化テキスト形式に割り当てる処理のことです。主な使用例として、感情分析、偽情報の検出や内容判定などが挙げられます。
# 
# 言語は本質的に曖昧で、変化し続け、適切に定義されていないため、テキスト分類は決して簡単なタスクではないが、深層学習による自然言語処理が発展したことにより、高精度化させることが可能になってきています。
# 
# とくに2018年に発表されたBERT {cite}`Devlin2019` はセンチメント分析を含めた多くのタスクに関して、当時の最高性能(SOTA: State of the Art)を達成する画期的な技術でした。
# 
# BERTは事前学習モデルの一種で、事前に一定のタスクに基づいて事前学習することで汎用性を獲得することに特徴があります。そのため、特定のタスクについてより少ないデータで性能を発揮することができます。 
# 
# BERTのような事前学習モデルによるテキスト分類の社会科学における応用可能性について多くの注目を集めています {cite}`laurer_van`。
# 
# ![](./Figure/text_class.png)
# 
# ### 今回のワークショップで扱うこと
# 
# 参加者は形態素解析やテキストデータの前処理など自然言語処理の基礎知識を持つ方を想定していますので、今回のワークショップは以下の内容を扱います：
# - 転移学習とファインチューニングによるテキスト分類の枠組
# - Hugging Face PyTorchインタフェース
# - Transformersによるセンチメント分析の実装
# 

# ## 転移学習とファインチューニング
# 
# 転移学習は、あるタスクの学習で得られた知識を、他の関連するタスクの学習に適用する手法を指します。一般的には、以下のステップで行われることが多いです：
# 
# - 事前学習: 事前学習モデル（pre-trained models)とは、大規模なデータセットを用いて訓練した学習済みモデルのことです。一般的に、大量のデータ（例えば、インターネット上のテキストデータ）を使用して、モデルを事前に学習します。この時点でのモデルは、言語の汎用的な特徴や構造を捉えることができます。
# 
# - ファインチューニング(fine-tuning): 事前学習モデルを、特定のタスクのデータ（例えば、感情分析や質問応答）でファインチューニングします。事前学習モデルでは汎用的な特徴をあらかじめ学習しておきますので、手元にある学習データが小規模でも高精度な認識性能を達成することが知られています。 
# 
# ![](./Figure/fine-tuning_methods.png)
# 
# ```{note} Transformerを用いるモデル
# 
# 2018年には、Self-Attentionと転移学習を組み合わせたTransformerとして、次の二つのモデルがリリースされました。
# 
# - GPT (Generative Pre-trained Transformer) は、Transformerアーキテクチャデコーダーのみを使用することで、単一のテキストデータを条件として次の単語を予測するというタスクを行います。
# - **BERT**（Bidirectional Encoder Representations from Transformers）は、Transformerアーキテクチャのエンコーダ部分を使用し、事前学習時に言語の広範な文脈を学ぶことができます。
#     - 入力テキストの情報は双方向に（すなわち、テキストの前後の文脈の両方を考慮した形で）エンコードされます。これが、BERTの「双方向性」の主な理由です。
#     -  事前学習の際の主なタスクは、マスクされた言語モデル (Masked Language Model, MLM) です。具体的には、入力テキストからランダムにいくつかの単語を「マスク」（隠す）し、そのマスクされた単語を正しく予測することを目的としてモデルを学習させます。
# ```

# In[ ]:





# ## 参考文献
# 
# ```{bibliography}
# ```
