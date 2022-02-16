from neuroglancer_json_schemas.url_state import parse_url_fragment, url_fragment_to_json
import urllib
import json

examples = {
    "empty_viewer": "http://neuroglancer-demo.appspot.com/#!%7B%22layers%22:%5B%7B%22type%22:%22new%22%2C%22source%22:%22%22%2C%22tab%22:%22source%22%2C%22name%22:%22new%20layer%22%7D%5D%2C%22selectedLayer%22:%7B%22visible%22:true%2C%22layer%22:%22new%20layer%22%7D%2C%22layout%22:%224panel%22%7D",
    "hemibrain": "https://hemibrain-dot-neuroglancer-demo.appspot.com/#!%7B%22dimensions%22:%7B%22x%22:%5B8e-9%2C%22m%22%5D%2C%22y%22:%5B8e-9%2C%22m%22%5D%2C%22z%22:%5B8e-9%2C%22m%22%5D%7D%2C%22position%22:%5B17114%2C20543%2C18610%5D%2C%22crossSectionScale%22:54.23751620061224%2C%22crossSectionDepth%22:-37.62185354999912%2C%22projectionScale%22:64770.91726975332%2C%22layers%22:%5B%7B%22type%22:%22image%22%2C%22source%22:%22precomputed://gs://neuroglancer-janelia-flyem-hemibrain/emdata/clahe_yz/jpeg%22%2C%22tab%22:%22source%22%2C%22name%22:%22emdata%22%7D%2C%7B%22type%22:%22segmentation%22%2C%22source%22:%22precomputed://gs://neuroglancer-janelia-flyem-hemibrain/v1.0/segmentation%22%2C%22tab%22:%22segments%22%2C%22name%22:%22segmentation%22%7D%2C%7B%22type%22:%22segmentation%22%2C%22source%22:%7B%22url%22:%22precomputed://gs://neuroglancer-janelia-flyem-hemibrain/v1.0/rois%22%2C%22subsources%22:%7B%22default%22:true%2C%22properties%22:true%2C%22mesh%22:true%7D%2C%22enableDefaultSubsources%22:false%7D%2C%22pick%22:false%2C%22tab%22:%22segments%22%2C%22selectedAlpha%22:0%2C%22saturation%22:0%2C%22objectAlpha%22:0.8%2C%22ignoreNullVisibleSet%22:false%2C%22meshSilhouetteRendering%22:3%2C%22colorSeed%22:2685294016%2C%22name%22:%22roi%22%7D%2C%7B%22type%22:%22annotation%22%2C%22source%22:%22precomputed://gs://neuroglancer-janelia-flyem-hemibrain/v1.0/synapses%22%2C%22tab%22:%22rendering%22%2C%22ignoreNullSegmentFilter%22:false%2C%22shader%22:%22#uicontrol%20vec3%20preColor%20color%28default=%5C%22red%5C%22%29%5Cn#uicontrol%20vec3%20postColor%20color%28default=%5C%22blue%5C%22%29%5Cn#uicontrol%20float%20preConfidence%20slider%28min=0%2C%20max=1%2C%20default=0%29%5Cn#uicontrol%20float%20postConfidence%20slider%28min=0%2C%20max=1%2C%20default=0%29%5Cn%5Cnvoid%20main%28%29%20%7B%5Cn%20%20setColor%28defaultColor%28%29%29%3B%5Cn%20%20setEndpointMarkerColor%28%5Cn%20%20%20%20vec4%28preColor%2C%200.5%29%2C%5Cn%20%20%20%20vec4%28postColor%2C%200.5%29%29%3B%5Cn%20%20setEndpointMarkerSize%282.0%2C%202.0%29%3B%5Cn%20%20setLineWidth%282.0%29%3B%5Cn%20%20if%20%28prop_pre_synaptic_confidence%28%29%3C%20preConfidence%20%7C%7C%5Cn%20%20%20%20%20%20prop_post_synaptic_confidence%28%29%3C%20postConfidence%29%20discard%3B%5Cn%7D%5Cn%22%2C%22linkedSegmentationLayer%22:%7B%22pre_synaptic_cell%22:%22segmentation%22%2C%22post_synaptic_cell%22:%22segmentation%22%7D%2C%22filterBySegmentation%22:%5B%22post_synaptic_cell%22%2C%22pre_synaptic_cell%22%5D%2C%22name%22:%22synapse%22%7D%2C%7B%22type%22:%22segmentation%22%2C%22source%22:%22precomputed://gs://neuroglancer-janelia-flyem-hemibrain/mito_20190717.27250582%22%2C%22pick%22:false%2C%22tab%22:%22segments%22%2C%22selectedAlpha%22:0.82%2C%22name%22:%22mito%22%2C%22visible%22:false%7D%2C%7B%22type%22:%22segmentation%22%2C%22source%22:%22precomputed://gs://neuroglancer-janelia-flyem-hemibrain/mask_normalized_round6%22%2C%22pick%22:false%2C%22tab%22:%22segments%22%2C%22selectedAlpha%22:0.53%2C%22segments%22:%5B%222%22%5D%2C%22name%22:%22mask%22%2C%22visible%22:false%7D%5D%2C%22showSlices%22:false%2C%22selectedLayer%22:%7B%22visible%22:true%2C%22layer%22:%22segmentation%22%7D%2C%22layout%22:%22xy-3d%22%2C%22selection%22:%7B%7D%7D",
    "fafb": "https://fafb-dot-neuroglancer-demo.appspot.com/#!%7B%22dimensions%22:%7B%22x%22:%5B4e-9%2C%22m%22%5D%2C%22y%22:%5B4e-9%2C%22m%22%5D%2C%22z%22:%5B4e-8%2C%22m%22%5D%7D%2C%22position%22:%5B109421.8984375%2C41044.6796875%2C5417%5D%2C%22crossSectionScale%22:2.1875%2C%22projectionOrientation%22:%5B-0.08939177542924881%2C-0.9848012924194336%2C-0.07470247149467468%2C0.12882165610790253%5D%2C%22projectionScale%22:27773.019357116023%2C%22layers%22:%5B%7B%22type%22:%22image%22%2C%22source%22:%22precomputed://gs://neuroglancer-fafb-data/fafb_v14/fafb_v14_orig%22%2C%22name%22:%22fafb_v14%22%2C%22visible%22:false%7D%2C%7B%22type%22:%22image%22%2C%22source%22:%22precomputed://gs://neuroglancer-fafb-data/fafb_v14/fafb_v14_clahe%22%2C%22name%22:%22fafb_v14_clahe%22%7D%2C%7B%22type%22:%22segmentation%22%2C%22source%22:%22precomputed://gs://fafb-ffn1-20190805/segmentation%22%2C%22segments%22:%5B%22710435991%22%5D%2C%22name%22:%22fafb-ffn1-20190805%22%7D%2C%7B%22type%22:%22annotation%22%2C%22source%22:%22precomputed://gs://neuroglancer-20191211_fafbv14_buhmann2019_li20190805%22%2C%22tab%22:%22rendering%22%2C%22annotationColor%22:%22#cecd11%22%2C%22shader%22:%22#uicontrol%20vec3%20preColor%20color%28default=%5C%22blue%5C%22%29%5Cn#uicontrol%20vec3%20postColor%20color%28default=%5C%22red%5C%22%29%5Cn#uicontrol%20float%20scorethr%20slider%28min=0%2C%20max=1000%29%5Cn#uicontrol%20int%20showautapse%20slider%28min=0%2C%20max=1%29%5Cn%5Cnvoid%20main%28%29%20%7B%5Cn%20%20setColor%28defaultColor%28%29%29%3B%5Cn%20%20setEndpointMarkerColor%28%5Cn%20%20%20%20vec4%28preColor%2C%200.5%29%2C%5Cn%20%20%20%20vec4%28postColor%2C%200.5%29%29%3B%5Cn%20%20setEndpointMarkerSize%285.0%2C%205.0%29%3B%5Cn%20%20setLineWidth%282.0%29%3B%5Cn%20%20if%20%28int%28prop_autapse%28%29%29%20%3E%20showautapse%29%20discard%3B%5Cn%20%20if%20%28prop_score%28%29%3Cscorethr%29%20discard%3B%5Cn%7D%5Cn%5Cn%22%2C%22shaderControls%22:%7B%22scorethr%22:80%7D%2C%22linkedSegmentationLayer%22:%7B%22pre_segment%22:%22fafb-ffn1-20190805%22%2C%22post_segment%22:%22fafb-ffn1-20190805%22%7D%2C%22filterBySegmentation%22:%5B%22post_segment%22%2C%22pre_segment%22%5D%2C%22name%22:%22synapses_buhmann2019%22%7D%2C%7B%22type%22:%22image%22%2C%22source%22:%22n5://gs://fafb-v14-synaptic-clefts-heinrich-et-al-2018-n5/synapses_dt_reblocked%22%2C%22opacity%22:0.73%2C%22shader%22:%22void%20main%28%29%20%7BemitRGBA%28vec4%280.0%2C0.0%2C1.0%2CtoNormalized%28getDataValue%28%29%29%29%29%3B%7D%22%2C%22name%22:%22clefts_Heinrich_etal%22%2C%22visible%22:false%7D%2C%7B%22type%22:%22segmentation%22%2C%22source%22:%22precomputed://gs://neuroglancer-fafb-data/elmr-data/FAFBNP.surf/mesh#type=mesh%22%2C%22segments%22:%5B%221%22%2C%2210%22%2C%2211%22%2C%2212%22%2C%2213%22%2C%2214%22%2C%2215%22%2C%2216%22%2C%2217%22%2C%2218%22%2C%2219%22%2C%222%22%2C%2220%22%2C%2221%22%2C%2222%22%2C%2223%22%2C%2224%22%2C%2225%22%2C%2226%22%2C%2227%22%2C%2228%22%2C%2229%22%2C%223%22%2C%2230%22%2C%2231%22%2C%2232%22%2C%2233%22%2C%2234%22%2C%2235%22%2C%2236%22%2C%2237%22%2C%2238%22%2C%2239%22%2C%224%22%2C%2240%22%2C%2241%22%2C%2242%22%2C%2243%22%2C%2244%22%2C%2245%22%2C%2246%22%2C%2247%22%2C%2248%22%2C%2249%22%2C%225%22%2C%2250%22%2C%2251%22%2C%2252%22%2C%2253%22%2C%2254%22%2C%2255%22%2C%2256%22%2C%2257%22%2C%2258%22%2C%2259%22%2C%226%22%2C%2260%22%2C%2261%22%2C%2262%22%2C%2263%22%2C%2264%22%2C%2265%22%2C%2266%22%2C%2267%22%2C%2268%22%2C%2269%22%2C%227%22%2C%2270%22%2C%2271%22%2C%2272%22%2C%2273%22%2C%2274%22%2C%2275%22%2C%228%22%2C%229%22%5D%2C%22name%22:%22neuropil-regions-surface%22%2C%22visible%22:false%7D%2C%7B%22type%22:%22mesh%22%2C%22source%22:%22vtk://https://storage.googleapis.com/neuroglancer-fafb-data/elmr-data/FAFB.surf.vtk.gz%22%2C%22shader%22:%22void%20main%28%29%20%7BemitRGBA%28vec4%281.0%2C%200.0%2C%200.0%2C%200.5%29%29%3B%7D%22%2C%22name%22:%22neuropil-full-surface%22%2C%22visible%22:false%7D%2C%7B%22type%22:%22segmentation%22%2C%22source%22:%5B%7B%22url%22:%22precomputed://gs://fafb-ffn1-20190805/segmentation%22%2C%22subsources%22:%7B%22default%22:true%2C%22bounds%22:true%7D%2C%22enableDefaultSubsources%22:false%7D%2C%22precomputed://gs://fafb-ffn1-20190805/segmentation/skeletons_32nm%22%5D%2C%22selectedAlpha%22:0%2C%22segments%22:%5B%224613663523%22%5D%2C%22name%22:%22skeletons_32nm%22%2C%22visible%22:false%7D%2C%7B%22type%22:%22segmentation%22%2C%22source%22:%22precomputed://gs://fafb-ffn1/fafb-public-skeletons%22%2C%22name%22:%22public_skeletons%22%2C%22visible%22:false%7D%5D%2C%22showAxisLines%22:false%2C%22showSlices%22:false%2C%22layout%22:%22xy-3d%22%7D",
    "mouse_cortex": "https://neuroglancer-demo.appspot.com/#!%7B%22dimensions%22:%7B%22x%22:%5B6.000000000000001e-9%2C%22m%22%5D%2C%22y%22:%5B6.000000000000001e-9%2C%22m%22%5D%2C%22z%22:%5B3.0000000000000004e-8%2C%22m%22%5D%7D%2C%22position%22:%5B5523.99072265625%2C8538.9384765625%2C1198.0423583984375%5D%2C%22crossSectionScale%22:3.7621853549999242%2C%22projectionOrientation%22:%5B-0.0040475670248270035%2C-0.9566215872764587%2C-0.22688281536102295%2C-0.18271005153656006%5D%2C%22projectionScale%22:4699.372698097029%2C%22layers%22:%5B%7B%22type%22:%22image%22%2C%22source%22:%22precomputed://gs://neuroglancer-public-data/kasthuri2011/image%22%2C%22tab%22:%22source%22%2C%22name%22:%22original-image%22%2C%22visible%22:false%7D%2C%7B%22type%22:%22image%22%2C%22source%22:%22precomputed://gs://neuroglancer-public-data/kasthuri2011/image_color_corrected%22%2C%22tab%22:%22source%22%2C%22name%22:%22corrected-image%22%7D%2C%7B%22type%22:%22segmentation%22%2C%22source%22:%22precomputed://gs://neuroglancer-public-data/kasthuri2011/ground_truth%22%2C%22tab%22:%22source%22%2C%22selectedAlpha%22:0.63%2C%22notSelectedAlpha%22:0.14%2C%22segments%22:%5B%2213%22%2C%2215%22%2C%222282%22%2C%223189%22%2C%223207%22%2C%223208%22%2C%223224%22%2C%223228%22%2C%223710%22%2C%223758%22%2C%224027%22%2C%22444%22%2C%224651%22%2C%224901%22%2C%224965%22%5D%2C%22name%22:%22ground_truth%22%7D%5D%2C%22layout%22:%224panel%22%7D",
    "medulla": "https://neuroglancer-demo.appspot.com/#!%7B%22dimensions%22:%7B%22x%22:%5B8e-9%2C%22m%22%5D%2C%22y%22:%5B8e-9%2C%22m%22%5D%2C%22z%22:%5B8e-9%2C%22m%22%5D%7D%2C%22position%22:%5B2914.500732421875%2C3088.243408203125%2C4045%5D%2C%22crossSectionScale%22:3.762185354999915%2C%22projectionOrientation%22:%5B0.31435418128967285%2C0.8142172694206238%2C0.4843378961086273%2C-0.06040274351835251%5D%2C%22projectionScale%22:4593.980956070107%2C%22layers%22:%5B%7B%22type%22:%22image%22%2C%22source%22:%22precomputed://gs://neuroglancer-public-data/flyem_fib-25/image%22%2C%22tab%22:%22source%22%2C%22name%22:%22image%22%7D%2C%7B%22type%22:%22segmentation%22%2C%22source%22:%22precomputed://gs://neuroglancer-public-data/flyem_fib-25/ground_truth%22%2C%22tab%22:%22source%22%2C%22segments%22:%5B%22158571%22%2C%2221894%22%2C%2222060%22%2C%2224436%22%2C%222515%22%5D%2C%22name%22:%22ground-truth%22%7D%5D%2C%22showSlices%22:false%2C%22layout%22:%224panel%22%7D",
}


def test_fragment_json():
    for name, example in examples.items():
        fragment = urllib.parse.urlparse(example).fragment
        fragment_json = url_fragment_to_json(fragment)
        vs = parse_url_fragment(fragment)
        vs_json = vs.json(exclude_unset=True)
        assert json.loads(vs_json) == json.loads(fragment_json)
