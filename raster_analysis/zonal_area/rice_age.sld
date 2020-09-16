<?xml version="1.0" encoding="UTF-8"?>
<StyledLayerDescriptor xmlns="http://www.opengis.net/sld" xmlns:gml="http://www.opengis.net/gml" version="1.0.0" xmlns:ogc="http://www.opengis.net/ogc" xmlns:sld="http://www.opengis.net/sld">
  <UserLayer>
    <sld:LayerFeatureConstraints>
      <sld:FeatureTypeConstraint/>
    </sld:LayerFeatureConstraints>
    <sld:UserStyle>
      <sld:Name>20180910_ricemap_dos_clip</sld:Name>
      <sld:FeatureTypeStyle>
        <sld:Rule>
          <sld:RasterSymbolizer>
            <sld:ChannelSelection>
              <sld:GrayChannel>
                <sld:SourceChannelName>1</sld:SourceChannelName>
              </sld:GrayChannel>
            </sld:ChannelSelection>
            <sld:ColorMap type="values">
              <sld:ColorMapEntry color="#f8f8fc" label="-103" quantity="-103"/>
              <sld:ColorMapEntry color="#3ca4f2" label="-102" quantity="-102"/>
              <sld:ColorMapEntry color="#ffe7cf" label="0" quantity="0"/>
              <sld:ColorMapEntry color="#feddbb" label="6" quantity="6"/>
              <sld:ColorMapEntry color="#fed2a6" label="12" quantity="12"/>
              <sld:ColorMapEntry color="#fdc38c" label="18" quantity="18"/>
              <sld:ColorMapEntry color="#fdb271" label="24" quantity="24"/>
              <sld:ColorMapEntry color="#fda25a" label="30" quantity="30"/>
              <sld:ColorMapEntry color="#fd9243" label="36" quantity="36"/>
              <sld:ColorMapEntry color="#fa812e" label="42" quantity="42"/>
              <sld:ColorMapEntry color="#f4701a" label="48" quantity="48"/>
              <sld:ColorMapEntry color="#ea5f0d" label="54" quantity="54"/>
              <sld:ColorMapEntry color="#df4f05" label="60" quantity="60"/>
              <sld:ColorMapEntry color="#cb4301" label="66" quantity="66"/>
              <sld:ColorMapEntry color="#b13902" label="72" quantity="72"/>
              <sld:ColorMapEntry color="#973003" label="78" quantity="78"/>
              <sld:ColorMapEntry color="#7f2704" label="90" quantity="90"/>
            </sld:ColorMap>
          </sld:RasterSymbolizer>
        </sld:Rule>
      </sld:FeatureTypeStyle>
    </sld:UserStyle>
  </UserLayer>
</StyledLayerDescriptor>
