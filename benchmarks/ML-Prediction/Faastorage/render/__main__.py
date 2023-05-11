import json
import numpy as np
import time


def timestamp(response, event, execute_start_time, execute_end_time, transport_start_time, transport_end_time):
    stamp_begin = 1000 * time.time()
    prior_execute_time = event['executeTime'] if 'executeTime' in event else 0
    response['executeTime'] = prior_execute_time + execute_end_time - execute_start_time

    prior_interaction_time = event['interactionTime'] if 'interactionTime' in event else 0
    response['interactionTime'] = prior_interaction_time + transport_end_time - transport_start_time

    prior_cost = event['timeStampCost'] if 'timeStampCost' in event else 0
    response['timeStampCost'] = prior_cost - (stamp_begin - 1000 * time.time())
    return response


def main(event):
    # execute function code
    # **********************************************************************************************************************
    execute_start_time = 1000 * time.time()
    body = json.loads(event['body'])
    x = np.array(body['predictions'])

    text = "Top 1 Prediction: " + str(x.argmax()) + str(x.max())
    print(text)

    response = {
        "statusCode": 200,
        "body": json.dumps({'render': text})
    }

    execute_end_time = 1000 * time.time()
    # **********************************************************************************************************************

    time_statistics = timestamp(response, event, execute_start_time, execute_end_time, 0, 0)

    response["executeTime"] = {
        "all": "{:.2f} ms".format(time_statistics["executeTime"]),
        "resize": "{:.2f} ms".format(event["resizeExecuteTime"]),
        "predict": "{:.2f} ms".format(event["predictExecuteTime"]),
        "render": "{:.2f} ms".format(execute_end_time - execute_start_time)
    }
    response["timeStampCost"] = "{:.2f} ms".format(time_statistics["timeStampCost"])
    response["interactionTime"] = "{:.2f} ms".format(time_statistics["interactionTime"])

    return response


if __name__ == '__main__':
    data = {
        'body': '{"predictions": [[0.00010830095561686903, 8.026276918826625e-05, 3.857371848425828e-05, 6.662449595751241e-05, 0.00010447922250023112, 4.469728810363449e-05, 4.3584746890701354e-05, 8.64645408000797e-05, 2.3388356567011215e-05, 6.807649333495647e-05, 2.522270369809121e-05, 5.26829571754206e-05, 7.451292913174257e-05, 3.375492451596074e-05, 3.343173739267513e-05, 7.93628569226712e-05, 2.960077836178243e-05, 2.598543869680725e-05, 7.124177500372753e-05, 0.00016855972353368998, 0.0004049681592732668, 7.076985639287159e-05, 7.513051241403446e-05, 6.478989234892651e-05, 3.242686216253787e-05, 7.238237594719976e-05, 5.379811773309484e-05, 4.716253897640854e-05, 0.00010679288243409246, 4.2740273784147575e-05, 0.00016769151261541992, 0.00011409587023081258, 7.220091356430203e-05, 0.00010016612213803455, 2.479401337041054e-05, 5.5568987590959296e-05, 9.195293387165293e-05, 9.448835771763697e-05, 2.347438748984132e-05, 8.949864422902465e-06, 5.0877748435596004e-05, 6.811033381382003e-05, 9.013649105327204e-05, 6.65165061946027e-05, 5.440300083137117e-05, 0.00018742858082987368, 0.00012246164260432124, 0.00011303729115752503, 5.9372054238338023e-05, 0.00014805358659941703, 2.977038275275845e-05, 1.550136585137807e-05, 1.8497796190786175e-05, 0.0002633414405863732, 5.5256987252505496e-05, 0.00011897756485268474, 9.128861711360514e-05, 0.0002451811742503196, 6.475629197666422e-05, 0.00011154460662510246, 0.00010265225864714012, 7.917900802567601e-05, 6.6748121753335e-05, 7.308481872314587e-05, 4.550403173197992e-05, 6.585991650354117e-05, 5.042686461820267e-05, 3.9175782148959115e-05, 0.00017697182192932814, 9.191637946059927e-05, 6.245823169592768e-05, 0.0006787265301682055, 1.8240127246826887e-05, 0.00012145858636358753, 0.0001481229264754802, 0.00017973987269215286, 7.039492629701272e-05, 0.00012794775830116123, 0.00011139141861349344, 7.363814802374691e-05, 0.0002363778476137668, 0.000156349953613244, 0.0002413159963907674, 4.7723850002512336e-05, 5.726223025703803e-05, 3.631054642028175e-05, 9.945650526788086e-05, 5.121994763612747e-05, 6.058371945982799e-05, 5.1565380999818444e-05, 0.0005003883270546794, 6.515802670037374e-05, 7.473874575225636e-05, 5.404825060395524e-05, 4.9547539674676955e-05, 9.007259905047249e-06, 3.945440039387904e-05, 2.9883709430578165e-05, 0.00016008270904421806, 4.110801819479093e-05, 6.831941573182121e-05, 6.316861981758848e-05, 0.0002970580826513469, 0.0002373152383370325, 1.0529027349548414e-05, 0.00010280685091856867, 0.0001783305633580312, 0.0002008505689445883, 0.00015724355762358755, 0.00013306224718689919, 6.468377250712365e-05, 0.00019533347222022712, 9.371469786856323e-05, 3.3138971048174426e-05, 5.575281102210283e-05, 5.1485236326698214e-05, 0.00011167200864292681, 4.392490882310085e-05, 0.00012030875950586051, 3.0330380468512885e-05, 7.521962106693536e-05, 0.0002457631635479629, 0.00011040837125619873, 1.3833337106916588e-05, 0.00019840158347506076, 8.709865505807102e-05, 4.698619886767119e-05, 4.654240910895169e-05, 0.0003288170846644789, 0.00023188085469882935, 2.8508982722996734e-05, 9.60182587732561e-05, 6.460029544541612e-05, 0.00011771418212447315, 2.0360115740913898e-05, 6.961090548429638e-05, 6.0933412896702066e-05, 6.976962322369218e-05, 9.043871978064999e-05, 7.129689765861258e-05, 6.320122338365763e-05, 8.434833580395207e-05, 3.297258444945328e-05, 8.495339716318995e-05, 0.00013166524877306074, 7.258269761223346e-05, 4.6515604481101036e-05, 0.0007401683833450079, 5.5820168199716136e-05, 0.00023208836500998586, 0.0001408095413353294, 6.904805195517838e-05, 4.2849365854635835e-05, 7.314883259823546e-05, 0.00011220384476473555, 3.875709080602974e-05, 4.110519148525782e-05, 5.364411117625423e-05, 0.00010027278767665848, 8.925066504161805e-05, 6.272840255405754e-05, 1.8893148080678657e-05, 0.00010234248475171626, 0.00015602701751049608, 4.68285106762778e-05, 0.00014634196122642606, 9.639158815843984e-05, 0.0005705021903850138, 8.55303296702914e-05, 6.020761065883562e-05, 1.2372929631965235e-05, 1.0797358299896587e-05, 5.1077167881885543e-05, 3.205669054295868e-05, 4.876235470874235e-05, 0.00017885465058498085, 1.599509414518252e-05, 1.9983153833891265e-05, 2.0469746232265607e-05, 2.7094714823761024e-05, 0.00027430144837126136, 0.00025983445812016726, 0.00016678098472766578, 4.499255373957567e-05, 6.511131505249068e-05, 3.9562233723700047e-05, 7.687455217819661e-05, 0.00027394486824050546, 2.4511395167792216e-05, 6.629231938859448e-05, 0.00044240301940590143, 0.00026196552789770067, 5.784771929029375e-05, 9.386165766045451e-05, 8.034110942389816e-05, 2.6338224415667355e-05, 0.00019615859491750598, 7.894203008618206e-05, 8.189655636670068e-05, 2.2200149032869376e-05, 0.00019326813344378024, 7.027693936834112e-05, 5.6611839681863785e-05, 7.513487798860297e-05, 0.00025295247905887663, 2.578612111392431e-05, 0.0001325169432675466, 0.00011876918870257214, 5.541186692425981e-05, 0.00018091201491188258, 2.2687567252432927e-05, 0.00010160717647522688, 6.895559636177495e-05, 0.0006459330907091498, 5.555489406106062e-05, 0.00012615152809303254, 4.426515442901291e-05, 0.0004785503842867911, 0.00018793009803630412, 3.906225902028382e-05, 0.00023189101193565875, 0.00012273769243620336, 3.50941154465545e-05, 0.00028587650740519166, 0.00022675140644423664, 0.000158154041855596, 0.00017919833771884441, 3.6479890695773065e-05, 8.047860319493338e-05, 0.00016472274728585035, 0.0007561430102214217, 2.337564728804864e-05, 7.486308459192514e-05, 0.00027939537540078163, 6.202326039783657e-05, 7.4350944487378e-05, 0.00010424781794426963, 5.8136862207902595e-05, 0.00010368751100031659, 0.00015433681255672127, 0.00019153638277202845, 7.263774750754237e-05, 6.291893078014255e-05, 2.6323861675336957e-05, 5.7874924095813185e-05, 4.636113590095192e-05, 0.0013334337854757905, 7.490842835977674e-05, 0.000125510836369358, 7.103458483470604e-05, 0.00019118160707876086, 9.877960110316053e-05, 0.0006067759823054075, 9.615883755031973e-05, 5.2243820391595364e-05, 0.00026844703825190663, 4.064339373144321e-05, 0.0006561069167219102, 0.00032792851561680436, 0.0003652304003480822, 3.289368760306388e-05, 0.00014389943680725992, 5.862575562787242e-05, 0.00022369157522916794, 8.128930494422093e-05, 0.00019032733689527959, 5.89162518735975e-05, 5.549500201595947e-05, 5.2554943977156654e-05, 4.232028004480526e-05, 4.868944233749062e-05, 0.00015911090304143727, 3.771276169572957e-05, 4.972358146915212e-05, 0.0003160275227855891, 6.937120633665472e-05, 0.00014672359975520521, 0.00011348610132699832, 4.312304736231454e-05, 0.00011122963769594207, 0.0004025926464237273, 3.489813389023766e-05, 3.596302485675551e-05, 0.00010965975525323302, 2.554264028731268e-05, 0.00013386998034548014, 9.457310079596937e-05, 7.498984632547945e-05, 7.492929580621421e-05, 0.00016947866242844611, 0.00016189574671443552, 0.0005196136771701276, 4.200699913781136e-05, 0.00012242392404004931, 5.985477764625102e-05, 0.0005458440282382071, 0.001820706413127482, 0.0016297617694362998, 4.743680256069638e-05, 0.00010989205475198105, 8.157587581081316e-05, 0.00010672771895769984, 5.784347013104707e-05, 8.003650873433799e-05, 0.00012024280295008793, 0.00015935175179038197, 0.0001478738122386858, 4.6865457989042625e-05, 6.351917545543984e-05, 4.060600622324273e-05, 0.00011096645903307945, 3.845093306154013e-05, 0.00018094464030582458, 9.016795956995338e-05, 0.00011920891847694293, 0.00010736638068920001, 0.00013360418961383402, 3.123255737591535e-05, 0.00018414761871099472, 7.321143493754789e-05, 9.132910781772807e-05, 0.0001895504246931523, 3.418736014282331e-05, 4.594168785843067e-05, 0.00011407574493205175, 0.0002719198237173259, 7.081421790644526e-05, 8.29813361633569e-05, 0.00013012249837629497, 0.00024640877381898463, 0.00012735660129692405, 0.0004551314632408321, 6.558413588209078e-05, 0.00016040440823417157, 4.6570734411943704e-05, 0.00013632833724841475, 3.8868172850925475e-05, 0.0004633914795704186, 3.872214074363001e-05, 0.0002827761636581272, 8.689886453794315e-05, 6.85714403516613e-05, 0.0008472127956338227, 0.0003250085574109107, 8.564264135202393e-05, 8.154367242241278e-05, 0.0001800534810172394, 7.19043382559903e-05, 0.00015196709136944264, 0.0023896663915365934, 0.0003511164104565978, 0.00011558708501979709, 0.00012935575796291232, 8.692978008184582e-05, 0.00012472261732909828, 1.7487442164565437e-05, 0.0002529739576857537, 4.591965625877492e-05, 7.17426955816336e-05, 6.859890709165484e-05, 2.838432374119293e-05, 9.918740397552028e-05, 0.00035315315471962094, 0.00030419588438235223, 8.530192280886695e-05, 3.9019181713229045e-05, 5.468264134833589e-05, 0.0003601251810323447, 0.00017268804367631674, 5.764038724009879e-05, 3.027951424883213e-05, 5.5720811360515654e-05, 0.0001016922906273976, 4.7211819037329406e-05, 4.220025584800169e-05, 0.00019234875799156725, 0.00042379429214634, 2.5016062863869593e-05, 3.626161196734756e-05, 7.154038758017123e-05, 2.592899909359403e-05, 2.0709792806883343e-05, 4.857187741436064e-05, 6.0227193898754194e-05, 0.00024476158432662487, 0.0003885201585944742, 0.00014495353389065713, 3.465913323452696e-05, 0.0005750046111643314, 0.8661227822303772, 8.051330223679543e-05, 6.559195026056841e-05, 5.2632334700319916e-05, 0.000240479304920882, 9.045450133271515e-05, 2.521572787372861e-05, 2.0433682948350906e-05, 5.641630559694022e-05, 5.696076186723076e-05, 5.849875378771685e-05, 5.14693783770781e-05, 0.00029992262716405094, 6.32978553767316e-05, 0.0001783487678039819, 8.877943037077785e-05, 0.00020644316100515425, 0.00015252229059115052, 6.375896919053048e-05, 2.410741217317991e-05, 5.1280112529639155e-05, 0.0003034361870959401, 9.606387175153941e-05, 0.000289336807327345, 0.00020226223568897694, 0.00011086089216405526, 7.100031507434323e-05, 6.741729885106906e-05, 0.00016613393381703645, 5.431907266029157e-05, 0.00015429590712301433, 1.9129842257825658e-05, 0.0002487851306796074, 4.5159002183936536e-05, 0.00019833688565995544, 3.419978384044953e-05, 2.270250115543604e-05, 0.00020476453937590122, 9.72753477981314e-05, 0.00031408085487782955, 0.00023917197540868074, 2.440200660203118e-05, 0.0002209040248999372, 5.223719199420884e-05, 0.00019149364379700273, 4.300201908336021e-05, 2.0071069229743443e-05, 0.0002653063856996596, 0.00011183624883415177, 5.2302446420071647e-05, 3.345055301906541e-05, 0.00011143296433147043, 0.00028497824678197503, 4.448364779818803e-05, 0.0001524109102319926, 0.00010410951654193923, 0.00013507057155948132, 0.0001507137349108234, 3.3110289223259315e-05, 0.00016561760276090354, 0.00018561103206593543, 6.48939676466398e-05, 7.490628922823817e-05, 0.0001863725046860054, 0.00013716728426516056, 0.00011558675760170445, 7.968046702444553e-05, 6.906188355060294e-05, 0.00038244109600782394, 6.53706956654787e-05, 0.00010216539521934465, 6.807773024775088e-05, 6.117528391769156e-05, 0.0005308119580149651, 3.2447649573441595e-05, 0.00039930918137542903, 0.00019972381414845586, 0.00018379217362962663, 0.000702702789567411, 2.075489283015486e-05, 4.190640538581647e-05, 0.0005929851904511452, 3.874692993122153e-05, 0.0004962346283718944, 0.00019151592277921736, 3.782557905651629e-05, 0.00014127344184089452, 0.0001937178458319977, 4.786857243743725e-05, 3.4676391805987805e-05, 7.015613664407283e-05, 0.00020183349261060357, 0.00014654264668934047, 0.0002611182280816138, 0.00016750753275118768, 0.00015305355191230774, 0.0001210660848300904, 9.632257570046932e-05, 0.00011868698493344709, 0.00017196018598042428, 0.00021699881472159177, 6.266329728532583e-05, 0.00022567187261302024, 0.00017937769007403404, 0.00012786127626895905, 5.65591108170338e-05, 5.5858508858364075e-05, 0.00017468715668655932, 0.00011057180381612852, 8.902182162273675e-05, 6.361016858136281e-05, 2.8358323106658645e-05, 0.00012593480641953647, 0.0002789161808323115, 0.00010211377230007201, 0.0002935444936156273, 7.467604882549495e-05, 3.6600078601622954e-05, 0.00011486632865853608, 8.009492012206465e-05, 8.641301974421367e-05, 6.583460344700143e-05, 4.822418122785166e-05, 7.412269042106345e-05, 2.518357359804213e-05, 0.00011090509360656142, 3.407437907299027e-05, 9.673554450273514e-05, 2.6824856831808574e-05, 9.505885827820748e-05, 7.266712782438844e-05, 2.8820646548410878e-05, 0.000254141166806221, 5.514448639587499e-05, 6.599062908207998e-05, 0.0002588767383713275, 0.0005124523304402828, 0.00017959457181859761, 0.00010929902055067942, 0.00011002407700289041, 0.00016691035125404596, 7.135880150599405e-05, 4.78580295748543e-05, 3.252677925047465e-05, 0.0001655277592362836, 0.0001094728140742518, 7.534921314800158e-05, 7.618987001478672e-05, 0.0001053105152095668, 3.658371133496985e-05, 8.852848986862227e-05, 0.0002019858075072989, 0.00014916057989466935, 9.241941734217107e-05, 0.00027788945590145886, 0.0002546722535043955, 0.00013095198664814234, 4.636546873371117e-05, 0.0002544198068790138, 7.275657844729722e-05, 0.00020296189177315682, 6.087335350457579e-05, 7.635513611603528e-05, 3.132461279165e-05, 8.213903493015096e-05, 0.00016296180547215044, 0.0001484631939092651, 7.84003350418061e-05, 2.9080978492856957e-05, 0.00013975812180433422, 0.00027574479463510215, 4.9021924496628344e-05, 0.0001907539990497753, 0.00013458594912663102, 9.664498793426901e-05, 0.000127986932056956, 5.527400935534388e-05, 0.00010664378351066262, 0.0001678577536949888, 0.00010054474114440382, 2.4138953449437395e-05, 3.953142004320398e-05, 0.00017643121827859432, 5.6615990615682676e-05, 7.840683974791318e-05, 0.00017926533473655581, 8.722134225536138e-05, 9.861696162261069e-05, 0.00014849477156531066, 6.678525096504018e-05, 6.563156057382002e-05, 0.00017916227807290852, 8.171852095983922e-05, 0.00024425139417871833, 2.2893240384291857e-05, 0.0004898125189356506, 4.49780527560506e-05, 2.719980329857208e-05, 9.415822569280863e-05, 2.3013020836515352e-05, 0.000324941793223843, 8.587451156927273e-05, 0.00011951671331189573, 0.00010847989324247465, 0.00020236468117218465, 4.83132571389433e-05, 0.00018387912132311612, 0.00028550243587233126, 8.099146361928433e-05, 0.0006542062619701028, 7.06719292793423e-05, 6.273468898143619e-05, 6.225562538020313e-05, 0.00012935155245941132, 4.608259041560814e-05, 8.923295536078513e-05, 3.303698395029642e-05, 0.00013076727918814868, 2.5472023480688222e-05, 0.0001673023944022134, 5.5985063227126375e-05, 5.6730899814283475e-05, 0.00010969154391204938, 9.636676986701787e-05, 4.273831655154936e-05, 3.5912267776438966e-05, 4.648097456083633e-05, 0.00011294463183730841, 4.801231261808425e-05, 2.2758775230613537e-05, 9.340989345218986e-05, 3.5964570997748524e-05, 3.182715590810403e-05, 0.00014230165106710047, 4.037001053802669e-05, 1.2353875717963092e-05, 3.833201481029391e-05, 6.065512206987478e-05, 0.00031117306207306683, 0.00013794611732009798, 0.00017866166308522224, 4.4114702177466825e-05, 5.24860224686563e-05, 8.719938341528177e-05, 4.087631168658845e-05, 5.1179125875933096e-05, 0.0002064136351691559, 0.000102144644188229, 7.259931589942425e-05, 7.136144995456561e-05, 8.318163600051776e-05, 6.502096221083775e-05, 0.0002068037720164284, 5.828969369758852e-05, 8.214263652916998e-05, 6.006469266139902e-05, 0.0001867813989520073, 5.043614510213956e-05, 7.984919648151845e-05, 2.3675496777286753e-05, 0.0003149246913380921, 0.00012663308007176965, 0.00010779646981973201, 0.0009382723947055638, 0.00012270176375750452, 0.0006311337347142398, 0.00048206967767328024, 0.0003793849318753928, 0.0001652022619964555, 0.00029603022267110646, 0.0001193506468553096, 0.00019554408208932728, 0.000185105818673037, 0.00011207327042939141, 4.210373663227074e-05, 6.506246427306905e-05, 6.050265801604837e-05, 3.708154690684751e-05, 0.00030905447783879936, 0.00015356350922957063, 4.1026203689398244e-05, 3.952260158257559e-05, 9.331773617304862e-05, 5.057534872321412e-05, 0.00018738248036243021, 5.593185414909385e-05, 4.729229840449989e-05, 6.497999129351228e-05, 0.0003364937729202211, 0.00016851794498506933, 3.499778904370032e-05, 6.312044570222497e-05, 7.393595296889544e-05, 5.934419823461212e-05, 6.273600592976436e-05, 0.00010750007641036063, 9.504643821856007e-05, 4.0492468542652205e-05, 0.00014112397911958396, 6.661337829427794e-05, 0.0006674911710433662, 0.00020110914192628115, 0.00025552348233759403, 0.00011173028906341642, 5.749363481299952e-05, 7.39592214813456e-05, 0.00011090456246165559, 8.683532360009849e-05, 3.068079240620136e-05, 6.983345519984141e-05, 0.00011884884588653222, 0.0001679059350863099, 5.1878254453185946e-05, 0.0001683152513578534, 0.00018785431166179478, 1.558758413011674e-05, 2.9723803891101852e-05, 0.00015302830433938652, 2.460350515320897e-05, 0.00010509951243875548, 4.135866038268432e-05, 6.304585258476436e-05, 2.4200680854846723e-05, 4.3880321754841134e-05, 0.00015110720414668322, 0.00014127008034847677, 0.00014699755411129445, 0.00022454396821558475, 7.790633389959112e-05, 0.00010252624633722007, 5.427252108347602e-05, 0.00032821635250002146, 8.626456110505387e-05, 0.00018185112276114523, 9.122808478423394e-06, 4.895455640507862e-05, 6.621277134399861e-05, 0.00013985970872454345, 3.736981670954265e-05, 2.2019741663825698e-05, 5.938796675764024e-05, 4.816778528038412e-05, 0.00026703145704232156, 0.00026664670440368354, 0.00017763584037311375, 0.00010011970880441368, 0.0001613582717254758, 9.129827958531678e-05, 0.00014943096903152764, 2.2779426217311993e-05, 0.00012007618352072313, 3.907157224602997e-05, 3.8514681364176795e-05, 8.705754589755088e-05, 0.00010686501627787948, 4.109570727450773e-05, 0.0001587584993103519, 0.00042504578595981, 6.667324487352744e-05, 2.8362217562971637e-05, 2.845397830242291e-05, 0.0001788648805813864, 3.457798084127717e-05, 0.00020138378022238612, 3.149664553347975e-05, 6.10063252679538e-05, 0.00027543649775907397, 0.00018650319543667138, 0.0003371055063325912, 0.00018810707842931151, 1.333045383944409e-05, 9.29071320570074e-05, 0.0003097964799962938, 5.82802458666265e-05, 7.343260949710384e-05, 0.0001405413495376706, 0.00016126089030876756, 0.00016125458932947367, 4.5802968088537455e-05, 3.333682980155572e-05, 4.9874226533574983e-05, 5.518594480236061e-05, 6.751162436557934e-05, 0.0004965873085893691, 0.0002718715986702591, 0.00015178241301327944, 7.244494190672413e-05, 3.226075932616368e-05, 0.00023100129328668118, 0.00024212629068642855, 2.656498327269219e-05, 0.0001298143615713343, 7.456140883732587e-05, 6.846590986242518e-05, 3.70439411199186e-05, 6.317313818726689e-05, 3.0066348699619994e-05, 8.190835069399327e-05, 9.882474114419892e-05, 0.00015707120473962277, 1.2522503311629407e-05, 0.00015359646931756288, 0.0002993081579916179, 0.00013565820700023323, 5.780007631983608e-05, 5.378072819439694e-05, 4.603866545949131e-05, 3.449267751420848e-05, 5.088624311611056e-05, 0.00011897529475390911, 0.00018554624693933874, 0.0003225589753128588, 7.185649883467704e-05, 8.819621871225536e-05, 9.73351052380167e-05, 5.179307845537551e-05, 4.93887418997474e-05, 0.0016664157155901194, 9.29445304791443e-05, 0.00014222771278582513, 4.5365766709437594e-05, 9.91981869447045e-05, 9.1618909209501e-05, 4.707033804152161e-05, 0.0009828060865402222, 5.522453284356743e-05, 4.0980921767186373e-05, 0.00023513633641414344, 8.123985753627494e-05, 4.625148358172737e-05, 6.031669181538746e-05, 0.0002499158727005124, 0.00037664262345060706, 0.00014705266221426427, 8.579739369452e-05, 0.0001106036506826058, 0.00018639382324181497, 0.00015025693573988974, 9.956944268196821e-05, 0.00014585111057385802, 2.092160502797924e-05, 0.00013679535186383873, 0.00014108415052760392, 5.1043618441326544e-05, 0.00018734458717517555, 0.0004541671951301396, 0.0004239543341100216, 8.75937839737162e-05, 0.00010483673395356163, 4.193659333395772e-05, 2.2170381271280348e-05, 0.00028796400874853134, 0.00010482044308446348, 7.635229121660814e-05, 0.00016288737242575735, 5.150090146344155e-05, 0.0001259239943465218, 2.9797707611578517e-05, 0.00015625127707608044, 0.0002163495373679325, 7.91239071986638e-05, 0.00013690498599316925, 0.00020122117712162435, 0.0001373986160615459, 6.297812069533393e-05, 3.9707003452349454e-05, 8.794534369371831e-05, 7.22032564226538e-05, 0.00010537410707911476, 3.4464828786440194e-05, 5.9060603234684095e-05, 7.417133747367188e-05, 4.853700738749467e-05, 8.218157745432109e-05, 9.191768913296983e-05, 0.00015489448560401797, 9.231406875187531e-05, 0.0001331259700236842, 7.69647813285701e-05, 9.708711877465248e-05, 0.0001523360697319731, 0.00020506784494500607, 5.6010481785051525e-05, 0.00012833344226237386, 7.70856931922026e-05, 0.00011533327779034153, 6.486420897999778e-05, 0.00011632490350166336, 0.0001552840694785118, 0.00012799182150047272, 0.0001794560521375388, 0.0001775621494743973, 5.9539946960285306e-05, 0.00011730816186172888, 1.59910832735477e-05, 6.961841427255422e-05, 4.7756901039974764e-05, 0.00018144265050068498, 0.00041068362770602107, 6.747963197994977e-05, 0.00019462074851617217, 0.00010410683898953721, 0.00010540445509832352, 7.250784256029874e-05, 1.7471005776314996e-05, 6.46930857328698e-05, 9.983777272282168e-05, 3.508283771225251e-05, 0.0003220601356588304, 5.443798363558017e-05, 5.9447233070386574e-05, 0.00017598607519175857, 5.063480421085842e-05, 0.000225569456233643, 8.284525392809883e-05, 3.790206028497778e-05, 8.84780238266103e-05, 9.430605859961361e-05, 5.061240153736435e-05, 0.00015999724564608186, 6.592162390006706e-05, 0.00014059657405596226, 0.0001713688689051196, 0.00010079858475364745, 8.480349060846493e-05, 0.00010819968883879483, 0.0002952319337055087, 0.00016339051944669336, 7.131967868190259e-05, 0.00013981717347633094, 0.00013287407637108117, 0.00012045110634062439, 0.00011694435670506209, 5.7413202739553526e-05, 5.071618943475187e-05, 2.2396876374841668e-05, 5.7145975006278604e-05, 8.149244240485132e-05, 0.00023911996686365455, 0.00013616669457405806, 0.00011074297071900219, 3.1979863706510514e-05, 3.125323564745486e-05, 8.640765736345202e-05, 0.00010173196642426774, 2.7943282475462183e-05, 4.1094412154052407e-05, 0.00011823554814327508, 0.00018766736320685595, 0.00011997385445283726, 0.0003749059687834233, 0.00041042795055545866, 0.00013539416249841452, 5.943998257862404e-05, 0.0007079790811985731, 5.955471351626329e-05, 5.131719444761984e-05, 4.3780961277661845e-05, 3.7255060306051746e-05, 0.00018651527352631092, 6.713371840305626e-05, 0.0001256211253348738, 3.421237488510087e-05, 6.766309525119141e-05, 5.580685683526099e-05, 0.00011106068996014073, 4.287352567189373e-05, 4.6704080887138844e-05, 0.00015772251936141402, 4.432733840076253e-05, 0.0002882698317989707, 0.0001301900192629546, 0.00013779188157059252, 0.00019720297132153064, 7.094589818734676e-05, 5.087706813355908e-05, 3.7454268749570474e-05, 5.938309550401755e-05, 0.00010475188901182264, 5.226340363151394e-05, 8.525994780939072e-05, 2.842265530489385e-05, 0.00011034426279366016, 7.950619328767061e-05, 0.00014337206084746867, 0.00015894589887466282, 6.775226211175323e-05, 0.0001638655230635777, 8.829915168462321e-05, 0.00012374304060358554, 7.150594319682568e-05, 0.0003942481707781553, 0.00011738257308024913, 7.349790394073352e-05, 5.0257676775800064e-05, 0.00011795904720202088, 0.00013181490066926926, 0.00012135647557443008, 9.580879122950137e-05, 6.093643605709076e-05, 4.103621904505417e-05, 3.105482755927369e-05, 0.0001449670671718195, 0.0002596932463347912, 6.988342647673562e-05, 0.0001473186566727236, 0.00019460683688521385, 0.0014360715867951512, 6.621119246119633e-05, 7.092681335052475e-05, 4.3358180846553296e-05, 0.00018565545906312764]]}',
        'statusCode': 200}
    print(json.dumps(data))
    print(main(data))
