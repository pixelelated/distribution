# T36 (#683) packet: EmulationStation's window, input and the rest of es-core at the pin 16dbac5211eea7e70db7394372033be2be7df829


## src/renderers/Renderer.cpp `:1141-1157` (an excerpt, upstream-carried, at the pin)

```text
 1141  			return 1.5f;  // GPI 320x240
 1142  
 1143  		if (sz >= 320 && sz < 720) // ODROID 480x320;
 1144  			return 1.31f;
 1145  
 1146  		return 1.0f;
 1147  	}
 1148  
 1149  	float ScreenSettings::fontScale()
 1150  	{
 1151  		auto scale = Settings::getInstance()->getString("FontScale");
 1152  		if (!scale.empty())
 1153  		{
 1154  			auto val = Utils::String::toFloat(scale);
 1155  			if (val > 0 && val < 4)
 1156  				return val;
 1157  		}
```

## src/resources/Font.cpp (whole, fork-modified, at the pin)

```text
    1  #include "resources/Font.h"
    2  #include "resources/TabStops.h"
    3  
    4  #include "renderers/Renderer.h"
    5  #include "utils/FileSystemUtil.h"
    6  #include "utils/StringUtil.h"
    7  #include "Log.h"
    8  #include "math/Misc.h"
    9  #include "LocaleES.h"
   10  
   11  #include "ResourceManager.h"
   12  #include "TextureResource.h"
   13  #include "Settings.h"
   14  #include "ImageIO.h"
   15  #include <algorithm>
   16  #include "math/Transform4x4f.h"
   17  
   18  #ifdef HAVE_FRIBIDI
   19  #include <fribidi.h>
   20  #endif
   21  
   22  #ifdef WIN32
   23  #include <Windows.h>
   24  #endif
   25  
   26  FT_Library Font::sLibrary = NULL;
   27  
   28  int Font::getSize() const { return mSize; }
   29  
   30  std::map< std::pair<std::string, int>, std::weak_ptr<Font> > Font::sFontMap;
   31  static std::map<unsigned int, std::string> substituableChars;
   32  
   33  Font::FontFace::FontFace(ResourceData&& d, int size) : data(d)
   34  {
   35  	int err = FT_New_Memory_Face(sLibrary, data.ptr.get(), (FT_Long)data.length, 0, &face);
   36  	if (!err)
   37  		FT_Set_Pixel_Sizes(face, 0, size);
   38  	else
   39  		face = nullptr;
   40  }
   41  
   42  Font::FontFace::~FontFace()
   43  {
   44  	if(face)
   45  		FT_Done_Face(face);
   46  }
   47  
   48  void Font::initLibrary()
   49  {
   50  	if (sLibrary != nullptr)
   51  		return;
   52  
   53  	if(FT_Init_FreeType(&sLibrary))
   54  	{
   55  		sLibrary = NULL;
   56  		LOG(LogError) << "Error initializing FreeType!";
   57  	}
   58  }
   59  
   60  size_t Font::getMemoryUsage() const
   61  {
   62  	size_t memUsage = 0;
   63  	
   64  	for(auto tex : mTextures)
   65  		memUsage += (tex->textureId != 0 ? tex->textureSize.x() * tex->textureSize.y() * 4 : 0);
   66  
   67  	for(auto it = mFaceCache.cbegin(); it != mFaceCache.cend(); it++)
   68  		memUsage += it->second->data.length;
   69  
   70  	return memUsage;
   71  }
   72  
   73  size_t Font::getTotalMemoryUsage()
   74  {
   75  	size_t total = 0;
   76  
   77  	auto it = sFontMap.cbegin();
   78  	while(it != sFontMap.cend())
   79  	{
   80  		if(it->second.expired())
   81  		{
   82  			it = sFontMap.erase(it);
   83  			continue;
   84  		}
   85  
   86  		total += it->second.lock()->getMemoryUsage();
   87  		it++;
   88  	}
   89  
   90  	return total;
   91  }
   92  
   93  Font::Font(int size, const std::string& path, bool menuScaling) : mSize(size), mPath(path)
   94  {
   95  	mSize = size;
   96  	//if(mSize > 160) mSize = 160; // maximize the font size while it is causing issues on linux
   97  
   98  	// GPI
   99  	float scale = menuScaling ? Renderer::ScreenSettings::menuFontScale() : Renderer::ScreenSettings::fontScale();
  100  	if (scale > 0.0f && scale != 1.0f)
  101  		mSize = size * scale;
  102  
  103  	if (mSize == 0)
  104  		mSize = 2;
  105  
  106  	mLoaded = true;
  107  	mMaxGlyphHeight = 0;
  108  
  109  	if(!sLibrary)
  110  		initLibrary();
  111  
  112  	for (unsigned int i = 0; i < 255; i++)
  113  		mGlyphCacheArray[i] = NULL;
  114  
  115  	// always initialize ASCII characters
  116  	for(unsigned int i = 32; i < 128; i++)
  117  		getGlyph(i);
  118  
  119  	clearFaceCache();
  120  }
  121  
  122  Font::~Font()
  123  {
  124  	unload();
  125  
  126  	for (auto tex : mTextures)
  127  		delete tex;
  128  
  129  	mTextures.clear();
  130  }
  131  
  132  void Font::reload()
  133  {
  134  	if (mLoaded)
  135  		return;
  136  	
  137  	Renderer::bindTexture(0);
  138  	rebuildTextures();
  139  	clearFaceCache();
  140  	Renderer::bindTexture(0);
  141  
  142  	mLoaded = true;
  143  }
  144  
  145  bool Font::unload()
  146  {
  147  	if (mLoaded)
  148  	{		
  149  		for (auto tex : mTextures)
  150  			tex->deinitTexture();
  151  
  152  		clearFaceCache();
  153  
  154  		mLoaded = false;
  155  		return true;
  156  	}
  157  
  158  	return false;
  159  }
  160  
  161  std::shared_ptr<Font> Font::get(int size, const std::string& path, bool menuScaling)
  162  {
  163  	const std::string canonicalPath = Utils::FileSystem::getCanonicalPath(path);
  164  
  165  	float scale = menuScaling ? Renderer::ScreenSettings::menuFontScale() : Renderer::ScreenSettings::fontScale();
  166  	int scaledSize = size * scale;
  167  
  168  	std::pair<std::string, int> def(canonicalPath.empty() ? getDefaultPath() : canonicalPath, scaledSize);
  169  	auto foundFont = sFontMap.find(def);
  170  	if(foundFont != sFontMap.cend())
  171  	{
  172  		if(!foundFont->second.expired())
  173  			return foundFont->second.lock();
  174  	}
  175  
  176  	std::shared_ptr<Font> font = std::shared_ptr<Font>(new Font(size, def.first, menuScaling));
  177  	sFontMap[def] = std::weak_ptr<Font>(font);
  178  	ResourceManager::getInstance()->addReloadable(font);
  179  	return font;
  180  }
  181  
  182  Font::FontTexture::FontTexture()
  183  {
  184  	textureId = 0;
  185  	textureSize = Vector2i(2048, 512);
  186  	writePos = Vector2i::Zero();
  187  	rowHeight = 0;
  188  }
  189  
  190  Font::FontTexture::~FontTexture()
  191  {
  192  	deinitTexture();
  193  }
  194  
  195  bool Font::FontTexture::findEmpty(const Vector2i& size, Vector2i& cursor_out)
  196  {
  197  	if(size.x() >= textureSize.x() || size.y() >= textureSize.y())
  198  		return false;
  199  
  200  	if(writePos.x() + size.x() >= textureSize.x() && writePos.y() + rowHeight + size.y() + 1 < textureSize.y())
  201  	{
  202  		// row full, but it should fit on the next row
  203  		// move cursor to next row
  204  		writePos = Vector2i(0, writePos.y() + rowHeight + 1); // leave 1px of space between glyphs
  205  		rowHeight = 0;
  206  	}
  207  
  208  	if(writePos.x() + size.x() >= textureSize.x() || writePos.y() + size.y() >= textureSize.y())
  209  	{
  210  		// nope, still won't fit
  211  		return false;
  212  	}
  213  
  214  	cursor_out = writePos;
  215  	writePos[0] += size.x() + 1; // leave 1px of space between glyphs
  216  
  217  	if(size.y() > rowHeight)
  218  		rowHeight = size.y();
  219  
  220  	return true;
  221  }
  222  
  223  void Font::FontTexture::initTexture()
  224  {
  225  	if (textureId == 0)
  226  	{
  227  		textureId = Renderer::createTexture(Renderer::Texture::ALPHA, true, false, textureSize.x(), textureSize.y(), nullptr);
  228  		if (textureId == 0)
  229  			LOG(LogError) << "FontTexture::initTexture() failed to create texture " << textureSize.x() << "x" << textureSize.y();
  230  	}
  231  }
  232  
  233  void Font::FontTexture::deinitTexture()
  234  {
  235  	if(textureId != 0)
  236  	{
  237  		Renderer::destroyTexture(textureId);
  238  		textureId = 0;
  239  	}
  240  }
  241  
  242  void Font::getTextureForNewGlyph(const Vector2i& glyphSize, FontTexture*& tex_out, Vector2i& cursor_out)
  243  {
  244  	if(mTextures.size())
  245  	{
  246  		// check if the most recent texture has space
  247  		tex_out = mTextures.back();
  248  
  249  		// will this one work?
  250  		if(tex_out->findEmpty(glyphSize, cursor_out))
  251  			return; // yes
  252  
  253  		LOG(LogDebug) << "Glyph texture cache full, creating a new texture cache for " << Utils::FileSystem::getFileName(mPath) << " " << mSize << "pt";
  254  	}
  255  
  256  	// current textures are full,
  257  	// make a new one
  258  	FontTexture* tex = new FontTexture();
  259  
  260  	int x = Math::min(2048, mSize * 64);
  261  	int y = Math::min(2048, Math::max(glyphSize.y(), mSize) + 2) * 1.2;
  262  
  263  	tex->textureSize = Vector2i(x, y);
  264  	tex->initTexture();
  265  
  266  	tex_out = tex;
  267  
  268  	mTextures.push_back(tex);
  269  	
  270  	bool ok = tex_out->findEmpty(glyphSize, cursor_out);
  271  	if(!ok)
  272  	{
  273  		LOG(LogError) << "Glyph too big to fit on a new texture (glyph size > " << tex_out->textureSize.x() << ", " << tex_out->textureSize.y() << ")!";
  274  		delete tex;
  275  		tex_out = NULL;
  276  	}
  277  }
  278  
  279  std::vector<std::string> getFallbackFontPaths()
  280  {
  281  	std::vector<std::string> fallbackFonts = 
  282  	{
  283  		":/fontawesome-webfont.ttf",
  284  		":/DroidSansFallbackFull.ttf",// japanese, chinese, present on Debian
  285  		":/PyeojinGothic-Medium.ttf", // korean font		
  286  		":/Vazirmatn-Regular.ttf", // arabic
  287  		":/Rubik-Regular.ttf" // hebrew (https://fontmeme.com/polices/police-rubik-hebrew public domain)
  288  	};
  289  
  290  	std::vector<std::string> paths;
  291  
  292  	for (auto font : fallbackFonts)
  293  		if (ResourceManager::getInstance()->fileExists(font))
  294  			paths.push_back(font);
  295  
  296  	paths.shrink_to_fit();
  297  	return paths;
  298  }
  299  
  300  #if defined(WIN32) || defined(X86) || defined(X86_64)
  301  static std::map<std::string, ResourceData> globalTTFCache;
  302  #endif
  303  
  304  FT_Face Font::getFaceForChar(unsigned int id)
  305  {
  306  	static const std::vector<std::string> fallbackFonts = getFallbackFontPaths();
  307  
  308  	// look through our current font + fallback fonts to see if any have the glyph we're looking for
  309  	for(unsigned int i = 0; i < fallbackFonts.size() + 1; i++)
  310  	{
  311  		auto fit = mFaceCache.find(i);
  312  
  313  		if(fit == mFaceCache.cend()) // doesn't exist yet
  314  		{
  315  			// i == 0 -> mPath
  316  			// otherwise, take from fallbackFonts
  317  			const std::string& path = (i == 0 ? mPath : fallbackFonts.at(i - 1));
  318  
  319  #if defined(WIN32) || defined(X86) || defined(X86_64)
  320  			auto itCache = globalTTFCache.find(path);
  321  			if (itCache == globalTTFCache.cend())
  322  			{
  323  				ResourceData dataX = ResourceManager::getInstance()->getFileData(path);
  324  				globalTTFCache.insert(std::pair<std::string, ResourceData>(path, dataX));
  325  				itCache = globalTTFCache.find(path);
  326  			}
  327  						
  328  			if (itCache == globalTTFCache.cend())
  329  				continue;
  330  
  331  			mFaceCache[i] = std::unique_ptr<FontFace>(new FontFace(std::move(itCache->second), mSize));
  332  #else
  333  			ResourceData data = ResourceManager::getInstance()->getFileData(path);
  334  			mFaceCache[i] = std::unique_ptr<FontFace>(new FontFace(std::move(data), mSize));
  335  #endif
  336  			fit = mFaceCache.find(i);
  337  		}
  338  
  339  		// i == 2 -> DroidSansFallbackFull
  340  		// this font has a bug when handling Korean characters.
  341  		if (i == 2 && Utils::String::isKorean(id))
  342  			continue;
  343  
  344  		if(FT_Get_Char_Index(fit->second->face, id) != 0)
  345  			return fit->second->face;
  346  	}
  347  
  348  	// nothing has a valid glyph - return the "real" face so we get a "missing" character
  349  	return mFaceCache.cbegin()->second->face;
  350  }
  351  
  352  void Font::clearFaceCache()
  353  {
  354  	mFaceCache.clear();
  355  }
  356  
  357  Font::Glyph* Font::getGlyph(unsigned int id)
  358  {
  359  	if (id < 255)
  360  	{
  361  		// FCA Optimisation : array is faster than a map
  362  		// When computing & displaying long descriptions in gamelist views, it can come here textsize*2 times per frame
  363  		Glyph* fastCache = mGlyphCacheArray[id];
  364  		if (fastCache != NULL)
  365  			return fastCache;
  366  	}
  367  	else
  368  	{
  369  		// is it already loaded?
  370  		auto it = mGlyphMap.find(id);
  371  		if (it != mGlyphMap.cend())
  372  			return it->second;
  373  	}
  374  
  375  	// nope, need to make a glyph
  376  	FT_Face face = getFaceForChar(id);
  377  	if(!face)
  378  	{
  379  		LOG(LogError) << "Could not find appropriate font face for character " << id << " for font " << mPath;
  380  		return NULL;
  381  	}
  382  
  383  	FT_GlyphSlot g = face->glyph;
  384  
  385  	if(FT_Load_Char(face, id, FT_LOAD_RENDER))
  386  	{
  387  		LOG(LogError) << "Could not find glyph for character " << id << " for font " << mPath << ", size " << mSize << "!";
  388  		return NULL;
  389  	}
  390  
  391  	Vector2i glyphSize(g->bitmap.width, g->bitmap.rows);
  392  
  393  	FontTexture* tex = NULL;
  394  	Vector2i cursor;
  395  	getTextureForNewGlyph(glyphSize, tex, cursor);
  396  
  397  	// getTextureForNewGlyph can fail if the glyph is bigger than the max texture size (absurdly large font size)
  398  	if(tex == NULL)
  399  	{
  400  		LOG(LogError) << "Could not create glyph for character " << id << " for font " << mPath << ", size " << mSize << " (no suitable texture found)!";
  401  		return NULL;
  402  	}
  403  
  404  	// create glyph
  405  	Glyph* pGlyph = new Glyph();
  406  	
  407  	pGlyph->texture = tex;
  408  	pGlyph->texPos = Vector2f((float)cursor.x() / (float)tex->textureSize.x(), (float)cursor.y() / (float)tex->textureSize.y());
  409  	pGlyph->texSize = Vector2f((float)glyphSize.x() / (float)tex->textureSize.x(), (float)glyphSize.y() / (float)tex->textureSize.y());
  410  	pGlyph->advance = Vector2f((float)g->metrics.horiAdvance / 64.0f, (float)g->metrics.vertAdvance / 64.0f);
  411  	pGlyph->bearing = Vector2f((float)g->metrics.horiBearingX / 64.0f, (float)g->metrics.horiBearingY / 64.0f);	
  412  	pGlyph->cursor = cursor;
  413  	pGlyph->glyphSize = glyphSize;
  414  
  415  	// upload glyph bitmap to texture
  416  	if (glyphSize.x() > 0 && glyphSize.y() > 0)
  417  		Renderer::updateTexture(tex->textureId, Renderer::Texture::ALPHA, cursor.x(), cursor.y(), glyphSize.x(), glyphSize.y(), g->bitmap.buffer);
  418  
  419  	// update max glyph height - Limit to ascii table. If we don't it can take in the fallback fonts
  420  	if (glyphSize.y() > mMaxGlyphHeight && id >= 32 && id < 128)
  421  		mMaxGlyphHeight = glyphSize.y();
  422  
  423  	mGlyphMap[id] = pGlyph;
  424  
  425  	if (id < 255)
  426  		mGlyphCacheArray[id] = pGlyph;
  427  
  428  	// done
  429  	return pGlyph;
  430  }
  431  
  432  // completely recreate the texture data for all textures based on mGlyphs information
  433  void Font::rebuildTextures()
  434  {
  435  	// recreate OpenGL textures
  436  	for(auto tex : mTextures)
  437  		tex->initTexture();
  438  
  439  	// reupload the texture data
  440  	for(auto it = mGlyphMap.cbegin(); it != mGlyphMap.cend(); it++)
  441  	{
  442  		FT_Face face = getFaceForChar(it->first);
  443  		FT_GlyphSlot glyphSlot = face->glyph;
  444  
  445  		// load the glyph bitmap through FT
  446  		FT_Load_Char(face, it->first, FT_LOAD_RENDER);
  447  
  448  		Glyph* glyph = it->second;
  449  		
  450  		// upload to texture
  451  		Renderer::updateTexture(glyph->texture->textureId, Renderer::Texture::ALPHA,
  452  			glyph->cursor.x(), glyph->cursor.y(),
  453  			glyph->glyphSize.x(), glyph->glyphSize.y(),
  454  			glyphSlot->bitmap.buffer);
  455  	}
  456  }
  457  
  458  void Font::renderSingleGlow(TextCache* cache, const Transform4x4f& parentTrans, float x, float y, bool verticesChanged)
  459  {
  460  	Transform4x4f trans = parentTrans;
  461  	trans.translate(x, y);
  462  	trans.round();
  463  	Renderer::setMatrix(trans);
  464  	renderTextCache(cache, verticesChanged);
  465  }
  466  
  467  void Font::renderTextCacheEx(TextCache* cache, const Transform4x4f& parentTrans, unsigned int mGlowSize, unsigned int mGlowColor, Vector2f& mGlowOffset, unsigned char mOpacity)
  468  {
  469  	if ((mGlowColor & 0x000000FF) != 0 && mGlowSize > 0)
  470  	{
  471  		Transform4x4f glowTrans = parentTrans;
  472  		glowTrans.translate(mGlowOffset.x(), mGlowOffset.y());
  473  		glowTrans.round();
  474  		Renderer::setMatrix(glowTrans);
  475  
  476  		auto copy = cache->vertexLists;
  477  
  478  		cache->setRenderingGlow(true);
  479  
  480  		if (mGlowSize == 1 && mGlowOffset == Vector2f::Zero())
  481  		{
  482  			int a = Math::min(0xFF, (mGlowColor & 0xFF) * 2);
  483  			cache->setColor((mGlowColor & 0xFFFFFF00) | (unsigned char)(a * (mOpacity / 255.0)));
  484  
  485  			renderSingleGlow(cache, glowTrans, 1, 0);
  486  			renderSingleGlow(cache, glowTrans, 0, 1, false);
  487  			renderSingleGlow(cache, glowTrans, -1, 0, false);
  488  			renderSingleGlow(cache, glowTrans, 0, -1, false);
  489  		}
  490  		else
  491  		{
  492  			cache->setColor((mGlowColor & 0xFFFFFF00) | (unsigned char)((mGlowColor & 0xFF) * (mOpacity / 255.0)));
  493  
  494  			int x = -mGlowSize;
  495  			int y = -mGlowSize;
  496  
  497  			renderSingleGlow(cache, glowTrans, x, y);
  498  
  499  			for (int i = 0; i < 2 * mGlowSize; i++)
  500  				renderSingleGlow(cache, glowTrans, ++x, y, false);
  501  
  502  			for (int i = 0; i < 2 * mGlowSize; i++)
  503  				renderSingleGlow(cache, glowTrans, x, ++y, false);
  504  
  505  			for (int i = 0; i < 2 * mGlowSize; i++)
  506  				renderSingleGlow(cache, glowTrans, --x, y, false);
  507  
  508  			for (int i = 0; i < 2 * mGlowSize; i++)
  509  				renderSingleGlow(cache, glowTrans, x, --y, false);
  510  		}
  511  
  512  		cache->setRenderingGlow(false);
  513  		cache->vertexLists = copy;
  514  	}
  515  
  516  	auto trans = parentTrans;
  517  	trans.round();
  518  	Renderer::setMatrix(trans);
  519  	renderTextCache(cache);
  520  }
  521  
  522  void Font::renderTextCache(TextCache* cache, bool verticesChanged)
  523  {
  524  	if(cache == NULL)
  525  	{
  526  		LOG(LogError) << "Attempted to draw NULL TextCache!";
  527  		return;
  528  	}
  529  
  530  	int tex = -1;
  531  
  532  	for(auto& vertex : cache->vertexLists)
  533  	{		
  534  		if (vertex.textureIdPtr == nullptr)
  535  			continue;
  536  		
  537  		if (tex != *vertex.textureIdPtr)
  538  		{
  539  			tex = *vertex.textureIdPtr;
  540  			Renderer::bindTexture(tex);			
  541  		}
  542  
  543  		if (tex != 0)
  544  		{
  545  			vertex.verts[0].customShader = cache->customShader.path.empty() ? nullptr : &cache->customShader;
  546  			Renderer::drawTriangleStrips(&vertex.verts[0], vertex.verts.size(), Renderer::Blend::SRC_ALPHA, Renderer::Blend::ONE_MINUS_SRC_ALPHA, cache->vertexLists.size() > 1 || verticesChanged);
  547  			vertex.verts[0].customShader = nullptr;
  548  		}
  549  	}
  550  
  551  	if (cache->renderingGlow || !verticesChanged)
  552  		return;
  553  
  554  	for (auto sub : cache->imageSubstitutes)
  555  	{
  556  		if (sub.texture && sub.texture->bind())
  557  		{
  558  			if (Settings::DebugImage())
  559  				Renderer::drawRect(
  560  					sub.vertex[0].pos.x(), 
  561  					sub.vertex[0].pos.y(), 
  562  					sub.vertex[3].pos.x() - sub.vertex[0].pos.x(),
  563  					sub.vertex[3].pos.x() - sub.vertex[0].pos.x(), 
  564  					0xFF000033, 0xFF000033);
  565  
  566  			Renderer::drawTriangleStrips(&sub.vertex[0], 4);
  567  		}
  568  	}
  569  }
  570  
  571  void Font::renderGradientTextCache(TextCache* cache, unsigned int colorTop, unsigned int colorBottom, bool horz)
  572  {
  573  	if (cache == NULL)
  574  	{
  575  		LOG(LogError) << "Attempted to draw NULL TextCache!";
  576  		return;
  577  	}
  578  
  579  	for (auto it = cache->vertexLists.cbegin(); it != cache->vertexLists.cend(); it++)
  580  	{
  581  		if (*it->textureIdPtr == 0)
  582  			continue;
  583  
  584  		std::vector<Renderer::Vertex> vxs;
  585  		vxs.resize(it->verts.size());
  586  
  587  		float maxY = -1;
  588  
  589  		for (int i = 0; i < it->verts.size(); i += 6)
  590  			if (maxY == -1 || maxY < it->verts[i + 2].pos.y())
  591  				maxY = it->verts[i + 2].pos.y();
  592  
  593  		for (int i = 0; i < it->verts.size(); i += 6)
  594  		{
  595  			float topOffset = it->verts[i + 1].pos.y();
  596  			float bottomOffset = it->verts[i + 2].pos.y();
  597  			
  598  			float topPercent = (maxY == 0 ? 1.0 : topOffset / maxY);
  599  			float bottomPercent = (maxY == 0 ? 1.0 : bottomOffset / maxY);
  600  
  601  			const unsigned int colorT = Renderer::mixColors(colorTop, colorBottom, topPercent);
  602  			const unsigned int colorB = Renderer::mixColors(colorTop, colorBottom, bottomPercent);
  603  		
  604  			vxs[i + 1] = it->verts[i + 1];
  605  			vxs[i + 1].col = colorT;
  606  
  607  			vxs[i + 2] = it->verts[i + 2];
  608  			vxs[i + 2].col = colorB;
  609  
  610  			vxs[i + 3] = it->verts[i + 3];
  611  			vxs[i + 3].col = colorT;
  612  
  613  			vxs[i + 4] = it->verts[i + 4];
  614  			vxs[i + 4].col = colorB;
  615  
  616  			// make duplicates of first and last vertex so this can be rendered as a triangle strip
  617  			vxs[i + 0] = vxs[i + 1];
  618  			vxs[i + 5] = vxs[i + 4];
  619  		}
  620  
  621  		Renderer::bindTexture(*it->textureIdPtr);
  622  		Renderer::drawTriangleStrips(&vxs[0], vxs.size());		
  623  	}
  624  }
  625  
  626  bool isBidiChar(char c)
  627  {
  628      return (c & 0xE0) == 0xC0 && (c & 0x10) == 0x10;
  629  }
  630  
  631  #ifdef HAVE_FRIBIDI
  632  std::string processRTLText(const std::string& text)
  633  {
  634      if (text.empty()) return text;
  635  
  636      size_t len = text.length();
  637  
  638      // 1. Convert UTF-8 to UTF-32 for FriBidi
  639      std::vector<FriBidiChar> unicode_in(len + 1);
  640      std::vector<FriBidiChar> unicode_out(len + 1);
  641      int ulen = fribidi_charset_to_unicode(FRIBIDI_CHAR_SET_UTF8, text.c_str(), len, unicode_in.data());
  642  
  643      // 2. Apply FriBidi for shaping + reorganisation BiDi
  644      FriBidiParType base_dir = FRIBIDI_PAR_RTL;
  645      fribidi_boolean ok = fribidi_log2vis(unicode_in.data(), ulen, &base_dir, unicode_out.data(), nullptr, nullptr, nullptr);
  646      if (!ok) return text;
  647  
  648      // 3. Convert UTF-32 to UTF-8 for es
  649      std::vector<char> utf8_out(len * 4 + 1);
  650      int out_len = fribidi_unicode_to_charset(FRIBIDI_CHAR_SET_UTF8, unicode_out.data(), ulen, utf8_out.data());
  651  
  652      return std::string(utf8_out.data(), out_len);
  653  }
  654  #endif
  655  
  656  std::string tryFastBidi(const std::string& text)
  657  {
  658      std::string ret = "";
  659  
  660      size_t lastCursor = 0;
  661      size_t i = 0;
  662      while (i < text.length())
  663      {
  664          const char&  c = text[i];
  665          
  666          if ((c & 0xE0) == 0xC0)
  667          {
  668              if (isBidiChar(c))
  669              {
  670                  ret.insert(lastCursor, text.substr(i + 1, 1));
  671                  ret.insert(lastCursor, text.substr(i, 1));
  672                  i += 2;
  673              }
  674              else
  675              {
  676                  ret += text[i++];
  677                  ret += text[i++];
  678                  lastCursor = i;
  679              }
  680          }
  681          else if ((c & 0xF0) == 0xE0)
  682          {
  683              ret += text[i++];
  684              ret += text[i++];
  685              ret += text[i++];
  686              lastCursor = i;
  687          }
  688          else if ((c & 0xF8) == 0xF0)
  689          {
  690              ret += text[i++];
  691              ret += text[i++];
  692              ret += text[i++];
  693              ret += text[i++];
  694              lastCursor = i;
  695          }
  696          else
  697          {
  698              if (c == 32 && i + 1 < text.length() && isBidiChar(text[i + 1]) && i > 1 && isBidiChar(text[i - 2]))
  699              {
  700                  ret.insert(lastCursor, text.substr(i, 1));
  701                  i++;
  702              }
  703              else
  704              {
  705                  ret += text[i++];
  706                  lastCursor = i;
  707              }
  708          }
  709      }
  710  
  711      return ret;
  712  }
  713  
  714  Vector2f Font::sizeText(const std::string& text, float lineSpacing)
  715  {
  716  	float lineWidth = 0.0f;
  717  	float highestWidth = 0.0f;
  718  
  719  	const float lineHeight = getHeight(lineSpacing);
  720  
  721  	float y = lineHeight;
  722  
  723  	size_t i = 0;
  724  	while(i < text.length())
  725  	{
  726  		unsigned int character = Utils::String::chars2Unicode(text, i); // advances i
  727  
  728  		if (substituableChars.find(character) != substituableChars.cend())
  729  		{
  730  			lineWidth += lineHeight;
  731  			continue;
  732  		}
  733  
  734  		if(character == '\n')
  735  		{
  736  			if(lineWidth > highestWidth)
  737  				highestWidth = lineWidth;
  738  
  739  			lineWidth = 0.0f;
  740  			y += lineHeight;
  741  		}
  742  
  743  		Glyph* glyph = getGlyph(character);
  744  		if(glyph)
  745  			lineWidth += glyph->advance.x();
  746  	}
  747  
  748  	if(lineWidth > highestWidth)
  749  		highestWidth = lineWidth;
  750  
  751  	return Vector2f(highestWidth, y);
  752  }
  753  
  754  float Font::getHeight(float lineSpacing) const
  755  {
  756  	return mMaxGlyphHeight * lineSpacing;
  757  }
  758  
  759  float Font::getLetterHeight()
  760  {
  761  	Glyph* glyph = getGlyph('S');
  762  	if (glyph != nullptr)
  763  		return glyph->glyphSize.y();
  764  
  765  	return mSize;
  766  }
  767  
  768  static inline bool isWhiteSpace(unsigned int c)
  769  {
  770  	return c == (unsigned int) ' ' || c == (unsigned int) '\n' || c == (unsigned int) '\t' || c == (unsigned int) '\v' || c == (unsigned int) '\f' || (unsigned int) c == '\r';
  771  }
  772  
  773  // Thanks eagle0wl'PR @ Retropie EmulationStation https://github.com/RetroPie/EmulationStation/pull/269/files
  774  // Breaks up a normal string with newlines to make it fit xLen
  775  std::string Font::wrapText(std::string text, float maxWidth)
  776  {
  777  	std::string out;
  778  
  779  	int lastCursor = 0;
  780  
  781  	while (text.length() > 0)  // find next cut-point
  782  	{
  783  		size_t cursor = 0;
  784  		float lineWidth = 0.0f;
  785  		size_t lastWhiteSpace = 0;
  786  		while (lineWidth < maxWidth && cursor < text.length())
  787  		{
  788  			lastCursor = cursor;
  789  			unsigned int c = Utils::String::chars2Unicode(text, cursor);
  790  
  791  			if (c == (unsigned int) '\n' || c == (unsigned int) '\r')
  792  				lineWidth = 0.0f;
  793  			else
  794  			{
  795  				Glyph* glyph = getGlyph(c);
  796  				if (glyph)
  797  					lineWidth += glyph->advance.x();
  798  			}
  799  						
  800  			if (isWhiteSpace(c))
  801  				lastWhiteSpace = cursor;			
  802  		}
  803  
  804  		if (cursor == text.length()) // arrived at end of text.
  805  		{
  806  			out += text;
  807  			text.erase();
  808  		}
  809  		else // need to cut at last whitespace or lacking that, the previous cursor.
  810  		{
  811  			size_t cut = (lastWhiteSpace != 0) ? lastWhiteSpace : lastCursor;
  812  			if (cut == 0)
  813  				break;
  814  
  815  			out += text.substr(0, cut) + "\n";
  816  			text.erase(0, cut);
  817  			lineWidth = 0.0f;
  818  		}
  819  	}
  820  
  821  	return out;
  822  }
  823  
  824  Vector2f Font::sizeWrappedText(const std::string& text, float xLen, float lineSpacing)
  825  {
  826  	auto wrapped = wrapText(text, xLen);
  827  	return sizeText(wrapped, lineSpacing);
  828  }
  829  
  830  // The gap a tab column keeps after the widest text before it.
  831  #define TAB_STOP_GAP (Renderer::getScreenWidth() * 0.01f)
  832  
  833  std::map<int, float> Font::getTabStops(const std::string& text, float lineSpacing)
  834  {
  835  	if (text.find('\t') == std::string::npos)
  836  		return std::map<int, float>();
  837  
  838  	// Each line is measured on its own, piece by piece between its tabs:
  839  	// the widths of what sits in each column, from which TabStops works the
  840  	// stops out column by column (#308 F-ES-11). The scan before this
  841  	// measured the run of text before each tab from the line's own start --
  842  	// right for one tab, and for two a stop that fell inside another line's
  843  	// column. The one before that walked the whole text once per line, so
  844  	// every stop was the FIRST line's ("Achievements (hardcore): ", "Succes
  845  	// (mode difficile): " ran into the value beside it).
  846  	const float lineHeight = getHeight(lineSpacing);
  847  
  848  	std::vector<std::vector<float>> columns;
  849  	for (auto line : Utils::String::split(text, '\n', true))
  850  	{
  851  		if (line.find('\t') == std::string::npos)
  852  			continue;
  853  
  854  		std::vector<float> pieces;
  855  		float width = 0.0f;
  856  
  857  		size_t pos = 0;
  858  		while (pos < line.length())
  859  		{
  860  			unsigned int character = Utils::String::chars2Unicode(line, pos); // also advances pos
  861  			if (character == 0 || character == '\r')
  862  				continue;
  863  
  864  			if (character == '\t')
  865  			{
  866  				pieces.push_back(width);   // the piece before this tab is a column
  867  				width = 0.0f;
  868  				continue;
  869  			}
  870  
  871  			if (substituableChars.find(character) != substituableChars.cend())
  872  			{
  873  				width += lineHeight;
  874  				continue;
  875  			}
  876  
  877  			Glyph* glyph = getGlyph(character);
  878  			if (glyph != NULL)
  879  				width += glyph->advance.x();
  880  		}
  881  		columns.push_back(pieces);   // what follows the last tab is no column's
  882  	}
  883  
  884  	return TabStops::fromColumns(columns, TAB_STOP_GAP);
  885  }
  886  
  887  Vector2f Font::sizeTabbedText(const std::string& text, float lineSpacing)
  888  {
  889  	// The same walk buildTextCache renders with, without the vertices: '\r'
  890  	// is nothing, '\n' a new line, a '\t' the jump to its stop.
  891  	const std::map<int, float> stops = getTabStops(text, lineSpacing);
  892  	const float lineHeight = getHeight(lineSpacing);
  893  
  894  	float lineWidth = 0.0f;
  895  	float highestWidth = 0.0f;
  896  	float y = lineHeight;
  897  	int tabIndex = 0;
  898  
  899  	size_t i = 0;
  900  	while (i < text.length())
  901  	{
  902  		unsigned int character = Utils::String::chars2Unicode(text, i); // also advances i
  903  		if (character == 0 || character == '\r')
  904  			continue;
  905  
  906  		if (character == '\n')
  907  		{
  908  			highestWidth = Math::max(highestWidth, lineWidth);
  909  			lineWidth = 0.0f;
  910  			y += lineHeight;
  911  			tabIndex = 0;
  912  			continue;
  913  		}
  914  
  915  		if (substituableChars.find(character) != substituableChars.cend())
  916  		{
  917  			lineWidth += lineHeight;
  918  			continue;
  919  		}
  920  
  921  		if (character == '\t')
  922  		{
  923  			auto it = stops.find(tabIndex);
  924  			tabIndex++;
  925  
  926  			if (it != stops.cend())
  927  			{
  928  				lineWidth = it->second + TAB_STOP_GAP;
  929  				continue;
  930  			}
  931  
  932  			character = ' ';
  933  		}
  934  
  935  		Glyph* glyph = getGlyph(character);
  936  		if (glyph != NULL)
  937  			lineWidth += glyph->advance.x();
  938  	}
  939  
  940  	return Vector2f(Math::max(highestWidth, lineWidth), y);
  941  }
  942  
  943  Vector2f Font::getWrappedTextCursorOffset(const std::string& text, float xLen, size_t stop, float lineSpacing)
  944  {
  945  	std::string wrappedText = wrapText(text, xLen);
  946  
  947  	float lineWidth = 0.0f;
  948  	float y = 0.0f;
  949  
  950  	size_t wrapCursor = 0;
  951  	size_t cursor = 0;
  952  	while(cursor < stop)
  953  	{
  954  		unsigned int wrappedCharacter = Utils::String::chars2Unicode(wrappedText, wrapCursor);
  955  		unsigned int character = Utils::String::chars2Unicode(text, cursor);
  956  
  957  		if(wrappedCharacter == '\n' && character != '\n')
  958  		{
  959  			//this is where the wordwrap inserted a newline
  960  			//reset lineWidth and increment y, but don't consume a cursor character
  961  			lineWidth = 0.0f;
  962  			y += getHeight(lineSpacing);
  963  
  964  			cursor = Utils::String::prevCursor(text, cursor); // unconsume
  965  			continue;
  966  		}
  967  
  968  		if(character == '\n')
  969  		{
  970  			lineWidth = 0.0f;
  971  			y += getHeight(lineSpacing);
  972  			continue;
  973  		}
  974  
  975  		Glyph* glyph = getGlyph(character);
  976  		if(glyph)
  977  			lineWidth += glyph->advance.x();
  978  	}
  979  
  980  	return Vector2f(lineWidth, y);
  981  }
  982  
  983  //=============================================================================================================
  984  //TextCache
  985  //=============================================================================================================
  986  
  987  float Font::getNewlineStartOffset(const std::string& text, const unsigned int& charStart, const float& xLen, const Alignment& alignment)
  988  {
  989  	switch(alignment)
  990  	{
  991  	case ALIGN_LEFT:
  992  		return 0;
  993  	case ALIGN_CENTER:
  994  		{
  995  			unsigned int endChar = (unsigned int)text.find('\n', charStart);
  996  			return (xLen - sizeText(text.substr(charStart, endChar != std::string::npos ? endChar - charStart : endChar)).x()) / 2.0f;
  997  		}
  998  	case ALIGN_RIGHT:
  999  		{
 1000  			unsigned int endChar = (unsigned int)text.find('\n', charStart);
 1001  			return xLen - (sizeText(text.substr(charStart, endChar != std::string::npos ? endChar - charStart : endChar)).x());
 1002  		}
 1003  	default:
 1004  		return 0;
 1005  	}
 1006  }
 1007  
 1008  TextCache* Font::buildTextCache(const std::string& _text, Vector2f offset, unsigned int color, float xLen, Alignment alignment, float lineSpacing)
 1009  {
 1010  	float x = offset[0] + (xLen != 0 ? getNewlineStartOffset(_text, 0, xLen, alignment) : 0);
 1011  	
 1012  	auto glyph = getGlyph('S');
 1013  	float yTop = glyph ? glyph->bearing.y() : 35;
 1014  	float yBot = getHeight(lineSpacing);
 1015  	float yDecal = (yBot + yTop) / 2.0f;
 1016  	float y = offset[1] + (yBot + yTop)/2.0f;
 1017  
 1018  	// vertices by texture
 1019  	std::map< FontTexture*, std::vector<Renderer::Vertex> > vertMap;
 1020  
 1021  #ifdef HAVE_FRIBIDI
 1022  	std::string text = EsLocale::isRTL() ? processRTLText(_text) : _text;
 1023  #else
 1024  	std::string text = EsLocale::isRTL() ? tryFastBidi(_text) : _text;
 1025  #endif
 1026  
 1027  	// A left-aligned text lines its tab columns up; centred or right-aligned,
 1028  	// a tab is a space (below).
 1029  	const std::map<int, float> tabStops = alignment == ALIGN_LEFT ? getTabStops(text, lineSpacing) : std::map<int, float>();
 1030  	int tabIndex = 0;
 1031  
 1032  	std::vector<TextImageSubstitute> imageSubstitutes;
 1033  
 1034  	bool inParenthesis = false;
 1035  	bool inBlock = false;
 1036  
 1037  	tabIndex = 0;
 1038  	size_t cursor = 0;
 1039  	while(cursor < text.length())
 1040  	{
 1041  		unsigned int character = Utils::String::chars2Unicode(text, cursor); // also advances cursor
 1042  
 1043  		auto it = substituableChars.find(character);
 1044  		if (it != substituableChars.cend() && ResourceManager::getInstance()->fileExists(it->second))
 1045  		{
 1046  			auto padding = (yTop / 4.0f);
 1047  
 1048  			//MaxSizeInfo mx(yBot - (2.0f * padding), yBot - (2.0f * padding));
 1049  
 1050  			TextImageSubstitute is;
 1051  			is.texture = TextureResource::get(it->second, true, true, true, false, true/*, &mx*/);
 1052  			if (is.texture != nullptr)
 1053  			{
 1054  				Renderer::Rect rect(
 1055  					x,
 1056  					y - yDecal + padding,
 1057  					yBot - (2.0f * padding),
 1058  					yBot - padding);
 1059  
 1060  				auto imgSize = is.texture->getPhysicalSize();
 1061  				auto sz = ImageIO::adjustPictureSize(Vector2i(imgSize.x(), imgSize.y()), Vector2i(rect.w, rect.h));
 1062  
 1063  				Renderer::Rect rc(
 1064  					rect.x + (rect.w / 2.0f) - (sz.x() / 2.0f), 
 1065  					rect.y + (rect.h / 2.0f) - (sz.y() / 2.0f),
 1066  					sz.x(),
 1067  					sz.y());
 1068  				
 1069  				unsigned int vertexColor = Renderer::convertColor(0xFFFFFF00 | (color & 0xFF));
 1070  				
 1071  				is.vertex[0] = { { (float) rc.x			, (float) rc.y + rc.h }	, { 0.0f, 0.0f }, vertexColor };
 1072  				is.vertex[1] = { { (float) rc.x			, (float) rc.y }		, { 0.0f, 1.0f }, vertexColor };
 1073  				is.vertex[2] = { { (float) rc.x + rc.w  , (float) rc.y + rc.h }	, { 1.0f, 0.0f }, vertexColor };
 1074  				is.vertex[3] = { { (float) rc.x + rc.w  , (float) rc.y }		, { 1.0f, 1.0f }, vertexColor };
 1075  
 1076  				imageSubstitutes.push_back(is);
 1077  
 1078  				x += yBot - (2.0f*padding);
 1079  				continue;
 1080  			}
 1081  		}
 1082  
 1083  		Glyph* glyph;
 1084  
 1085  		// invalid character
 1086  		if (character == 0)
 1087  			continue;
 1088  
 1089  		if (character == '\r')
 1090  			continue;
 1091  
 1092  		if(character == '\n')
 1093  		{
 1094  			tabIndex = 0;
 1095  			y += getHeight(lineSpacing);
 1096  			x = offset[0] + (xLen != 0 ? getNewlineStartOffset(text, (const unsigned int)cursor /* cursor is already advanced */, xLen, alignment) : 0);
 1097  			continue;
 1098  		}
 1099  
 1100  		if (character == '\t')
 1101  		{
 1102  			auto it = tabStops.find(tabIndex);
 1103  			if (it != tabStops.cend())
 1104  			{
 1105  				x = offset[0] + it->second + TAB_STOP_GAP;
 1106  				tabIndex++;
 1107  				continue;
 1108  			}
 1109  
 1110  			character = ' ';
 1111  			tabIndex++;
 1112  		}
 1113  
 1114  		if (character == '(')
 1115  			inParenthesis = true;
 1116  		else if (character == ')')
 1117  			inParenthesis = false;
 1118  
 1119  		if (character == '[')
 1120  			inBlock = true;
 1121  		else if (character == ']')
 1122  			inBlock = false;
 1123  
 1124  		glyph = getGlyph(character);
 1125  		if(glyph == NULL)
 1126  			continue;
 1127  
 1128  		std::vector<Renderer::Vertex>& verts = vertMap[glyph->texture];
 1129  		size_t oldVertSize = verts.size();
 1130  		verts.resize(oldVertSize + 6);
 1131  		Renderer::Vertex* vertices = verts.data() + oldVertSize;
 1132  
 1133  		const float        glyphStartX    = x + glyph->bearing.x();
 1134  		const unsigned int convertedColor = Renderer::convertColor(color);
 1135  
 1136  		vertices[1] = { { glyphStartX                                       , y - glyph->bearing.y()                                          }, { glyph->texPos.x(),                      glyph->texPos.y()                      }, convertedColor };
 1137  		vertices[2] = { { glyphStartX                                       , y - glyph->bearing.y() + (glyph->glyphSize.y())                 }, { glyph->texPos.x(),                      glyph->texPos.y() + glyph->texSize.y() }, convertedColor };
 1138  		vertices[3] = { { glyphStartX + glyph->glyphSize.x()                , y - glyph->bearing.y()                                          }, { glyph->texPos.x() + glyph->texSize.x(), glyph->texPos.y()                      }, convertedColor };
 1139  		vertices[4] = { { glyphStartX + glyph->glyphSize.x()                , y - glyph->bearing.y() + (glyph->glyphSize.y())                 }, { glyph->texPos.x() + glyph->texSize.x(), glyph->texPos.y() + glyph->texSize.y() }, convertedColor };
 1140  
 1141  		// round vertices
 1142  		for (int i = 1; i < 5; ++i)
 1143  		{
 1144  			vertices[i].pos.round();
 1145  
 1146  			if (inParenthesis || inBlock || character == ']' || character == ')')
 1147  				vertices[i].saturation = 0.0f;
 1148  			else
 1149  				vertices[i].saturation = 1.0f;
 1150  		}
 1151  
 1152  		// make duplicates of first and last vertex so this can be rendered as a triangle strip
 1153  		vertices[0] = vertices[1];
 1154  		vertices[5] = vertices[4];
 1155  
 1156  		// advance
 1157  		x += glyph->advance.x();
 1158  	}
 1159  
 1160  	//TextCache::CacheMetrics metrics = { sizeText(text, lineSpacing) };
 1161  
 1162  	TextCache* cache = new TextCache();
 1163  	cache->vertexLists.resize(vertMap.size());
 1164  	cache->metrics = { sizeText(text, lineSpacing) };
 1165  	cache->imageSubstitutes = imageSubstitutes;
 1166  
 1167  	unsigned int i = 0;
 1168  	for(auto it = vertMap.cbegin(); it != vertMap.cend(); it++)
 1169  	{
 1170  		TextCache::VertexList& vertList = cache->vertexLists.at(i);
 1171  
 1172  		vertList.textureIdPtr = &it->first->textureId;
 1173  		vertList.verts = it->second;
 1174  		i++;
 1175  	}
 1176  
 1177  	clearFaceCache();
 1178  
 1179  	return cache;
 1180  }
 1181  
 1182  TextCache* Font::buildTextCache(const std::string& text, float offsetX, float offsetY, unsigned int color)
 1183  {
 1184  	return buildTextCache(text, Vector2f(offsetX, offsetY), color, 0.0f);
 1185  }
 1186  
 1187  void TextCache::setColors(unsigned int color, unsigned int extraColor)
 1188  {
 1189  	const unsigned int convertedColor = Renderer::convertColor(color);
 1190  	const unsigned int convertedExtraColor = Renderer::convertColor(extraColor);
 1191  
 1192  	for (auto it = vertexLists.begin(); it != vertexLists.end(); it++)
 1193  	{
 1194  		for (auto it2 = it->verts.begin(); it2 != it->verts.end(); it2++)
 1195  		{
 1196  			if (!renderingGlow && it2->saturation == 0)
 1197  				it2->col = convertedExtraColor;
 1198  			else
 1199  				it2->col = convertedColor;
 1200  		}
 1201  	}
 1202  
 1203  	if (renderingGlow)
 1204  		return;
 1205  
 1206  	unsigned int substitColor = Renderer::convertColor(0xFFFFFF00 | (color & 0xFF));
 1207  
 1208  	for (TextImageSubstitute& it : imageSubstitutes)
 1209  		for (int i = 0; i < 4; i++)
 1210  			it.vertex[i].col = substitColor;
 1211  }
 1212  
 1213  void TextCache::setColor(unsigned int color)
 1214  {
 1215  	const unsigned int convertedColor = Renderer::convertColor(color);
 1216  
 1217  	for (auto it = vertexLists.begin(); it != vertexLists.end(); it++)
 1218  		for (auto it2 = it->verts.begin(); it2 != it->verts.end(); it2++)
 1219  				it2->col = convertedColor;
 1220  	
 1221  	if (renderingGlow)
 1222  		return;
 1223  
 1224  	unsigned int substitColor = Renderer::convertColor(0xFFFFFF00 | (color & 0xFF));
 1225  
 1226  	for (TextImageSubstitute& it : imageSubstitutes)
 1227  		for (int i = 0; i < 4; i++)
 1228  			it.vertex[i].col = substitColor;
 1229  }
 1230  
 1231  std::shared_ptr<Font> Font::getFromTheme(const ThemeData::ThemeElement* elem, unsigned int properties, const std::shared_ptr<Font>& orig, bool menu)
 1232  {
 1233  	using namespace ThemeFlags;
 1234  	if(!(properties & FONT_PATH) && !(properties & FONT_SIZE))
 1235  		return orig;
 1236  	
 1237  	std::shared_ptr<Font> font;
 1238  	int size = (orig ? orig->mSize : FONT_SIZE_MEDIUM);
 1239  	std::string path = (orig ? orig->mPath : getDefaultPath());
 1240  
 1241  	float sh = (float) Math::min(Renderer::getScreenHeight(), Renderer::getScreenWidth());
 1242  	if(properties & FONT_SIZE && elem->has("fontSize")) 
 1243  	{
 1244  		if ((int)(sh * elem->get<float>("fontSize")) > 0)
 1245  			size = (int)(sh * elem->get<float>("fontSize"));
 1246  	}
 1247  
 1248  	if(properties & FONT_PATH && elem->has("fontPath"))
 1249  	{
 1250  		std::string tmppath = elem->get<std::string>("fontPath");
 1251  		if (!tmppath.empty())
 1252  			path = tmppath;
 1253  	}
 1254  
 1255  	return get(size, path, menu);
 1256  }
 1257  
 1258  void Font::OnThemeChanged()
 1259  {
 1260  	static std::map<unsigned int, std::string> defaultMap =
 1261  	{
 1262  		{ 0xF300, ":/flags/au.png" },
 1263  		{ 0xF301, ":/flags/br.png" },
 1264  		{ 0xF302, ":/flags/ca.png" },
 1265  		{ 0xF303, ":/flags/cn.png" },
 1266  		{ 0xF304, ":/flags/de.png" },
 1267  		{ 0xF305, ":/flags/es.png" },
 1268  		{ 0xF306, ":/flags/eu.png" },
 1269  		{ 0xF307, ":/flags/fr.png" },
 1270  		{ 0xF308, ":/flags/gr.png" },
 1271  		{ 0xF309, ":/flags/in.png" },
 1272  		{ 0xF30A, ":/flags/it.png" },
 1273  		{ 0xF30B, ":/flags/jp.png" },
 1274  		{ 0xF30C, ":/flags/kr.png" },
 1275  		{ 0xF30D, ":/flags/nl.png" },
 1276  		{ 0xF30E, ":/flags/no.png" },
 1277  		{ 0xF30F, ":/flags/pt.png" },
 1278  		{ 0xF310, ":/flags/ru.png" },
 1279  		{ 0xF311, ":/flags/sw.png" },
 1280  		{ 0xF312, ":/flags/uk.png" },
 1281  		{ 0xF313, ":/flags/us.png" },
 1282  		{ 0xF314, ":/flags/wr.png" }
 1283  	};
 1284  
 1285  	substituableChars = defaultMap;
 1286  
 1287  	auto paths = ResourceManager::getInstance()->getResourcePaths();
 1288  	std::reverse(paths.begin(), paths.end());
 1289  
 1290  	for (auto testPath : paths)
 1291  	{
 1292  		auto fontoverrides = Utils::FileSystem::combine(testPath, "fontoverrides");
 1293  		for (auto file : Utils::FileSystem::getDirectoryFiles(fontoverrides))
 1294  		{
 1295  			if (file.directory || file.hidden)
 1296  				continue;
 1297  
 1298  			if (Utils::String::toLower(Utils::FileSystem::getExtension(file.path)) != ".png")
 1299  				continue;
 1300  
 1301  			auto stem = Utils::FileSystem::getStem(file.path);
 1302  
 1303  			auto val = Utils::String::fromHexString(stem);
 1304  			if (val >= 0xF000)
 1305  			{
 1306  				substituableChars.erase(val);
 1307  				substituableChars.insert(std::pair<unsigned int, std::string>(val, file.path));
 1308  			}
 1309  		}
 1310  	}
 1311  }
```

## src/resources/Font.h (whole, fork-modified, at the pin)

```text
    1  #pragma once
    2  #ifndef ES_CORE_RESOURCES_FONT_H
    3  #define ES_CORE_RESOURCES_FONT_H
    4  
    5  #include "math/Vector2f.h"
    6  #include "math/Vector2i.h"
    7  #include "renderers/Renderer.h"
    8  #include "resources/ResourceManager.h"
    9  #include "ThemeData.h"
   10  #include <ft2build.h>
   11  #include FT_FREETYPE_H
   12  #include <vector>
   13  #include <unordered_map>
   14  
   15  class TextCache;
   16  class TextureResource;
   17  
   18  #define FONT_SIZE_MINI ((unsigned int)(0.030f * Math::min((int)Renderer::getScreenHeight(), (int)Renderer::getScreenWidth())))
   19  #define FONT_SIZE_SMALL ((unsigned int)(0.035f * Math::min((int)Renderer::getScreenHeight(), (int)Renderer::getScreenWidth())))
   20  #define FONT_SIZE_MEDIUM ((unsigned int)(0.045f * Math::min((int)Renderer::getScreenHeight(), (int)Renderer::getScreenWidth())))
   21  #define FONT_SIZE_LARGE ((unsigned int)(0.085f * Math::min((int)Renderer::getScreenHeight(), (int)Renderer::getScreenWidth())))
   22  
   23  #ifdef WIN32
   24  #define FONT_PATH_LIGHT ":/opensans_hebrew_condensed_light.ttf"
   25  #define FONT_PATH_REGULAR ":/opensans_hebrew_condensed_regular.ttf"
   26  #else
   27  #define FONT_PATH_LIGHT ":/ubuntu_condensed.ttf" 
   28  #define FONT_PATH_REGULAR ":/ubuntu_condensed.ttf" 
   29  #endif
   30  
   31  enum Alignment
   32  {
   33  	ALIGN_LEFT = 0,
   34  	ALIGN_CENTER = 1, // centers both horizontally and vertically
   35  	ALIGN_RIGHT = 2,
   36  	ALIGN_TOP = 3,
   37  	ALIGN_BOTTOM = 4
   38  };
   39  
   40  
   41  //A TrueType Font renderer that uses FreeType and OpenGL.
   42  //The library is automatically initialized when it's needed.
   43  class Font : public IReloadable
   44  {
   45  public:
   46  	static void initLibrary();
   47  
   48  	static std::shared_ptr<Font> get(int size, const std::string& path = getDefaultPath(), bool menuScaling = false);
   49  	static void OnThemeChanged();
   50  
   51  	virtual ~Font();
   52  
   53  	Vector2f sizeText(const std::string& text, float lineSpacing = 1.5f); // Returns the expected size of a string when rendered.  Extra spacing is applied to the Y axis.
   54  	TextCache* buildTextCache(const std::string& text, float offsetX, float offsetY, unsigned int color);
   55  	TextCache* buildTextCache(const std::string& text, Vector2f offset, unsigned int color, float xLen, Alignment alignment = ALIGN_LEFT, float lineSpacing = 1.5f);
   56  	
   57  	void renderTextCache(TextCache* cache, bool verticesChanged = true);
   58  	void renderTextCacheEx(TextCache* cache, const Transform4x4f& parentTrans, unsigned int mGlowSize, unsigned int mGlowColor, Vector2f& mGlowOffset, unsigned char mOpacity = 255);
   59  
   60  	void renderGradientTextCache(TextCache* cache, unsigned int colorTop, unsigned int colorBottom, bool horz = false);
   61  	
   62  	std::string wrapText(std::string text, float xLen); // Inserts newlines into text to make it wrap properly.
   63  	Vector2f sizeWrappedText(const std::string& text, float xLen, float lineSpacing = 1.5f); // Returns the expected size of a string after wrapping is applied.
   64  	// The size of a left-aligned text as buildTextCache lays it out, tabs
   65  	// included: a '\t' jumps to its column's stop (the widest text before
   66  	// that tab on any line, plus a gap), where sizeText() measures it as a
   67  	// glyph and does not know where the text after it lands. A page that puts
   68  	// something beside a tabbed block measures the block here (#160).
   69  	Vector2f sizeTabbedText(const std::string& text, float lineSpacing = 1.5f);
   70  	Vector2f getWrappedTextCursorOffset(const std::string& text, float xLen, size_t cursor, float lineSpacing = 1.5f); // Returns the position of of the cursor after moving "cursor" characters.
   71  
   72  	float getHeight(float lineSpacing = 1.5f) const;
   73  	float getLetterHeight();
   74  
   75  	bool unload() override;
   76  	void reload() override;
   77  
   78  	int getSize() const;
   79  	inline const std::string& getPath() const { return mPath; }
   80  
   81  	inline static const char* getDefaultPath() { return FONT_PATH_REGULAR; }
   82  
   83  	static std::shared_ptr<Font> getFromTheme(const ThemeData::ThemeElement* elem, unsigned int properties, const std::shared_ptr<Font>& orig, bool menu = false);
   84  
   85  	size_t getMemoryUsage() const; // returns an approximation of VRAM used by this font's texture (in bytes)
   86  	static size_t getTotalMemoryUsage(); // returns an approximation of total VRAM used by font textures (in bytes)
   87  
   88  private:
   89  	void renderSingleGlow(TextCache* cache, const Transform4x4f& parentTrans, float x, float y, bool verticesChanged = true);
   90  
   91  	static FT_Library sLibrary;
   92  	static std::map< std::pair<std::string, int>, std::weak_ptr<Font> > sFontMap;
   93  
   94  	Font(int size, const std::string& path, bool menuScaling = false);
   95  
   96  	class FontTexture
   97  	{
   98  	public:
   99  		unsigned int textureId;
  100  		Vector2i textureSize;
  101  
  102  		Vector2i writePos;
  103  		int rowHeight;
  104  
  105  		FontTexture();
  106  		~FontTexture();
  107  		bool findEmpty(const Vector2i& size, Vector2i& cursor_out);
  108  
  109  		// you must call initTexture() after creating a FontTexture to get a textureId
  110  		void initTexture(); // initializes the OpenGL texture according to this FontTexture's settings, updating textureId
  111  		void deinitTexture(); // deinitializes the OpenGL texture if any exists, is automatically called in the destructor
  112  	};
  113  
  114  	struct FontFace
  115  	{
  116  		const ResourceData data;
  117  		FT_Face face;
  118  
  119  		FontFace(ResourceData&& d, int size);
  120  		virtual ~FontFace();
  121  	};
  122  
  123  	void rebuildTextures();
  124  
  125  	std::vector<FontTexture*> mTextures;
  126  
  127  	void getTextureForNewGlyph(const Vector2i& glyphSize, FontTexture*& tex_out, Vector2i& cursor_out);
  128  
  129  	std::map< unsigned int, std::unique_ptr<FontFace> > mFaceCache;
  130  	FT_Face getFaceForChar(unsigned int id);
  131  	void clearFaceCache();
  132  
  133  	struct Glyph
  134  	{
  135  		FontTexture* texture;
  136  		
  137  		Vector2f texPos;
  138  		Vector2f texSize; // in texels!
  139  
  140  		Vector2f advance;
  141  		Vector2f bearing;
  142  
  143  		Vector2i cursor;
  144  		Vector2i glyphSize;
  145  	};
  146  
  147  	Glyph* mGlyphCacheArray[255]; // used to cache 255 first chars
  148  	std::unordered_map<unsigned int, Glyph*> mGlyphMap;
  149  
  150  	Glyph* getGlyph(unsigned int id);
  151  
  152  	int mMaxGlyphHeight;
  153  	
  154  	int mSize;
  155  	const std::string mPath;
  156  	bool mLoaded;
  157  
  158  	float getNewlineStartOffset(const std::string& text, const unsigned int& charStart, const float& xLen, const Alignment& alignment);
  159  	// One stop per tab column, in pixels from the start of a line: the widest
  160  	// first column, then each stop the last plus the gap plus its own column's
  161  	// widest text (TabStops::fromColumns). Empty when the text has no tab.
  162  	std::map<int, float> getTabStops(const std::string& text, float lineSpacing);
  163  
  164  	friend TextCache;
  165  };
  166  
  167  struct TextImageSubstitute
  168  {
  169  	//Vector2f pos;
  170  	//Vector2f size;
  171  	// unsigned int character;
  172  
  173  	Renderer::Vertex vertex[4];
  174  	std::shared_ptr<TextureResource> texture;
  175  };
  176  
  177  // Used to store a sort of "pre-rendered" string.
  178  // When a TextCache is constructed (Font::buildTextCache()), the vertices and texture coordinates of the string are calculated and stored in the TextCache object.
  179  // Rendering a previously constructed TextCache (Font::renderTextCache) every frame is MUCH faster than rebuilding one every frame.
  180  // Keep in mind you still need the Font object to render a TextCache (as the Font holds the OpenGL texture), and if a Font changes your TextCache may become invalid.
  181  class TextCache
  182  {
  183  protected:
  184  
  185  	struct VertexList
  186  	{
  187  		std::vector<Renderer::Vertex> verts;
  188  		unsigned int* textureIdPtr; // this is a pointer because the texture ID can change during deinit/reinit (when launching a game)
  189  	};
  190  
  191  	std::vector<VertexList> vertexLists;
  192  	std::vector<TextImageSubstitute> imageSubstitutes;
  193  	bool renderingGlow;
  194  
  195  	Renderer::ShaderInfo customShader;
  196  
  197  public:
  198  	TextCache()
  199  	{
  200  		renderingGlow = false;
  201  	}
  202  
  203  	struct CacheMetrics
  204  	{
  205  		Vector2f size;
  206  	} metrics;
  207  
  208  	void setColor(unsigned int color);
  209  	void setColors(unsigned int color, unsigned int extraColor);
  210  
  211  	void setRenderingGlow(bool glow) { renderingGlow = glow; }
  212  	void setCustomShader(Renderer::ShaderInfo* shader) { if (shader == nullptr) customShader.path = ""; else customShader = *shader; }
  213  
  214  	friend Font;
  215  };
  216  
  217  #endif // ES_CORE_RESOURCES_FONT_H
```

## src/resources/TabStops.h (whole, fork-added, at the pin)

```text
    1  #pragma once
    2  #ifndef ES_CORE_RESOURCES_TAB_STOPS_H
    3  #define ES_CORE_RESOURCES_TAB_STOPS_H
    4  
    5  #include <map>
    6  #include <vector>
    7  
    8  // Where a tabbed text's columns start, from what is in them (Font's
    9  // getTabStops, sizeTabbedText and buildTextCache): pure, so es-unit-tests
   10  // reaches it without a font (es-app/tests/unit/TabStopsTests.cpp).
   11  namespace TabStops
   12  {
   13  	// `lines` holds, for each line, the width of each piece before a tab --
   14  	// the piece after a line's last tab is no column's and is not listed.
   15  	// The answer is one stop per tab index, in pixels from the line's start:
   16  	// text after tab k is drawn at stop k plus `gap`.
   17  	//
   18  	// Column by column (#308 F-ES-11): stop 0 is the widest first column,
   19  	// and each later stop is the one before it plus the gap plus the widest
   20  	// text in its own column -- because that is where the drawing puts the
   21  	// column, at the previous stop plus the gap. The stops used to be the
   22  	// widest run of text before each tab measured along each line from its
   23  	// own start, which is right for one tab and wrong for two: a short first
   24  	// column beside a long second one gave a second stop that fell inside
   25  	// another line's second column, and its third column was drawn over it.
   26  	inline std::map<int, float> fromColumns(const std::vector<std::vector<float>>& lines, float gap)
   27  	{
   28  		std::vector<float> widest;
   29  		for (auto& pieces : lines)
   30  		{
   31  			if (pieces.size() > widest.size())
   32  				widest.resize(pieces.size(), 0.0f);
   33  			for (size_t k = 0; k < pieces.size(); k++)
   34  				if (pieces[k] > widest[k])
   35  					widest[k] = pieces[k];
   36  		}
   37  
   38  		std::map<int, float> stops;
   39  		float x = 0.0f;
   40  		for (size_t k = 0; k < widest.size(); k++)
   41  		{
   42  			x += (k == 0 ? 0.0f : gap) + widest[k];
   43  			stops[(int) k] = x;
   44  		}
   45  		return stops;
   46  	}
   47  }
   48  
   49  #endif // ES_CORE_RESOURCES_TAB_STOPS_H
```

## src/resources/TextureData.cpp (whole, fork-modified, at the pin)

```text
    1  #include "resources/TextureData.h"
    2  
    3  #include "math/Misc.h"
    4  #include "renderers/Renderer.h"
    5  #include "resources/ResourceManager.h"
    6  #include "ImageIO.h"
    7  #include "Log.h"
    8  #include <nanosvg/nanosvg.h>
    9  #include <nanosvg/nanosvgrast.h>
   10  #include <string.h>
   11  #include <algorithm>
   12  #include <vlc/vlc.h>
   13  
   14  #include "Settings.h"
   15  #include "utils/ZipFile.h"
   16  #include "utils/StringUtil.h"
   17  #include "utils/FileSystemUtil.h"
   18  #include "utils/StringListLock.h"
   19  #include "Paths.h"
   20  
   21  #define DPI 96
   22  
   23  #define OPTIMIZEVRAM Settings::getInstance()->getBool("OptimizeVRAM")
   24  
   25  IPdfHandler* TextureData::PdfHandler = nullptr;
   26  
   27  TextureData::TextureData(bool tile, bool linear) : 
   28  	mTile(tile), mLinear(linear), mTextureID(0), mDataRGBA(nullptr), mScalable(false), mDynamic(true), mReloadable(false),
   29  #if defined(USE_OPENGLES_30)
   30  	mMipmapped(false),
   31  #endif
   32  	mSize(Vector2i::Zero()), mPhysicalSize(Vector2f::Zero()), mMaxSize(MaxSizeInfo::Empty)
   33  {
   34  	mIsExternalDataRGBA = false;
   35  	mRequired = false;
   36  }
   37  
   38  TextureData::~TextureData()
   39  {
   40  	releaseVRAM();
   41  	releaseRAM();
   42  }
   43  
   44  #if defined(USE_OPENGLES_30)
   45  size_t TextureData::getMemoryUsage(MemoryUsageType type)
   46  {
   47  	const size_t width = mSize.x() > 0 ? static_cast<size_t>(mSize.x()) : 0;
   48  	const size_t height = mSize.y() > 0 ? static_cast<size_t>(mSize.y()) : 0;
   49  	const size_t baseSize = width * height * 4;
   50  
   51  	bool accountForMipmaps = mMipmapped;
   52  	if (type == MemoryUsageType::Estimated && !accountForMipmaps)
   53  	{
   54  		accountForMipmaps = mReloadable && !mIsExternalDataRGBA && mLinear && !mTile &&
   55  			!Utils::FileSystem::isVideo(mPath) && (mSize.x() >= 256 || mSize.y() >= 256);
   56  	}
   57  
   58  	size_t textureSize = baseSize;
   59  	if (accountForMipmaps && width > 0 && height > 0)
   60  	{
   61  		textureSize = 0;
   62  		size_t levelWidth = width;
   63  		size_t levelHeight = height;
   64  		while (true)
   65  		{
   66  			textureSize += levelWidth * levelHeight * 4;
   67  			if (levelWidth == 1 && levelHeight == 1)
   68  				break;
   69  			levelWidth = std::max<size_t>(1, levelWidth / 2);
   70  			levelHeight = std::max<size_t>(1, levelHeight / 2);
   71  		}
   72  	}
   73  
   74  	if (type == MemoryUsageType::RAM)
   75  		return mDataRGBA != nullptr ? baseSize : 0;
   76  	if (type == MemoryUsageType::VRAM)
   77  		return mTextureID != 0 ? textureSize : 0;
   78  	if (type == MemoryUsageType::Estimated)
   79  		return textureSize;
   80  	return mTextureID != 0 ? textureSize : (mDataRGBA != nullptr ? baseSize : 0);
   81  }
   82  #endif
   83  
   84  void TextureData::initFromPath(const std::string& path)
   85  {
   86  	// Just set the path. It will be loaded later
   87  	mPath = path;
   88  	// Only textures with paths are reloadable
   89  	mReloadable = true;
   90  }
   91  
   92  bool TextureData::initSVGFromMemory(const unsigned char* fileData, size_t length)
   93  {
   94  	// If already initialised then don't read again
   95  	std::unique_lock<std::mutex> lock(mMutex);
   96  	if (mDataRGBA || (mTextureID != 0))
   97  		return true;
   98  
   99  	// nsvgParse excepts a modifiable, null-terminated string
  100  	char* copy = (char*)malloc(length + 1);
  101  	if (copy == NULL)
  102  		return false;
  103  	
  104  	memcpy(copy, fileData, length);
  105  	copy[length] = '\0';
  106  
  107  	NSVGimage* svgImage = nsvgParse(copy, "px", DPI);
  108  	free(copy);
  109  	if (!svgImage)
  110  	{
  111  		LOG(LogError) << "Error parsing SVG image.";
  112  		return false;
  113  	}
  114  
  115  	if (svgImage->width == 0 || svgImage->height == 0)
  116  	{
  117  		nsvgDelete(svgImage);
  118  		return false;
  119  	}
  120  
  121  	float sourceWidth = svgImage->width;
  122  	float sourceHeight = svgImage->height;
  123  
  124  	if (mScalableMinimumSize.empty())
  125  	{
  126  		sourceWidth = svgImage->width;
  127  		sourceHeight = svgImage->height;
  128  		
  129  		if (!mMaxSize.empty() && sourceWidth < mMaxSize.x() && sourceHeight < mMaxSize.y())
  130  		{
  131  			auto sz = ImageIO::adjustPictureSizeF(sourceWidth, sourceHeight, mMaxSize.x(), mMaxSize.y(), mMaxSize.externalZoom());
  132  			sourceHeight = sz.y();
  133  			sourceWidth = (sourceHeight * svgImage->width) / svgImage->height; // FCA : Always compute width using source aspect ratio
  134  		}
  135  	}
  136  	else
  137  	{
  138  		sourceHeight = mScalableMinimumSize.y();
  139  		sourceWidth = (sourceHeight * svgImage->width) / svgImage->height; // FCA : Always compute width using source aspect ratio
  140  	}
  141  
  142  	mScalableMinimumSize = Vector2f(sourceWidth, sourceHeight);
  143  	mPhysicalSize = Vector2f(sourceWidth, sourceHeight);
  144  
  145  	size_t width = (size_t)Math::round(sourceWidth);
  146  	size_t height = (size_t)Math::round(sourceHeight);
  147  
  148  	if (width == 0)
  149  	{
  150  		// auto scale width to keep aspect
  151  		width = (size_t)Math::round(((float)height / svgImage->height) * svgImage->width);
  152  	}
  153  	else if (height == 0)
  154  	{
  155  		// auto scale height to keep aspect
  156  		height = (size_t)Math::round(((float)width / svgImage->width) * svgImage->height);
  157  	}
  158  
  159  	if (OPTIMIZEVRAM && !mMaxSize.empty() && (width > mMaxSize.x() || height > mMaxSize.y()))
  160  	{
  161  		auto imageSize = Vector2i(width, height);
  162  		auto displaySize = Vector2i((int)Math::round(mMaxSize.x()), (int)Math::round(mMaxSize.y()));
  163  
  164  		Vector2i sz = ImageIO::adjustPictureSize(imageSize, displaySize, mMaxSize.externalZoom());
  165  		if (sz.x() == displaySize.x())
  166  		{
  167  			width = sz.x();
  168  			height = Math::round((width * svgImage->height) / svgImage->width);
  169  		}
  170  		else
  171  		{
  172  			height = sz.y();
  173  			width = Math::round((height * svgImage->width) / svgImage->height);
  174  		}
  175  	}
  176  	
  177  	mSize = Vector2i(width, height);
  178  
  179  	if (width * height <= 0)
  180  	{
  181  		LOG(LogError) << "Error parsing SVG image size.";
  182  		return false;
  183  	}
  184  
  185  	if (!mTile)
  186  	{
  187  		// Record what was rasterised, not what was asked for. The clamp above can
  188  		// leave the bitmap smaller than the request, and rasterizeAt decides whether
  189  		// to re-rasterise by comparing the next request against these two; holding
  190  		// the pre-clamp size here made a larger request look already satisfied, so a
  191  		// logo first drawn by a game list header at 157x50 stayed 157x50 when the
  192  		// system view asked for 384x122, and was GPU-upscaled soft (#181). A tiled
  193  		// texture keeps the old bookkeeping: its bitmap size is its tile pitch.
  194  		mScalableMinimumSize = Vector2f((float)width, (float)height);
  195  		mPhysicalSize = mScalableMinimumSize;
  196  	}
  197  
  198  	unsigned char* dataRGBA = new unsigned char[width * height * 4];
  199  
  200  	double scale = ((float)((int)height)) / svgImage->height;
  201  	double scaleV = ((float)((int)width)) / svgImage->width;
  202  	if (scaleV < scale)
  203  		scale = scaleV;
  204  
  205  	NSVGrasterizer* rast = nsvgCreateRasterizer();
  206  	nsvgRasterize(rast, svgImage, 0, 0, scale, dataRGBA, (int)width, (int)height, (int)width * 4);
  207  	nsvgDeleteRasterizer(rast);
  208  	nsvgDelete(svgImage);
  209  
  210  	ImageIO::flipPixelsVert(dataRGBA, width, height);
  211  
  212  	mDataRGBA = dataRGBA;
  213  
  214  	return true;
  215  }
  216  
  217  bool TextureData::initImageFromMemory(const unsigned char* fileData, size_t length, int subImageIndex)
  218  {
  219  	if (length == 0)
  220  		return false;
  221  
  222  	// If already initialised then don't read again
  223  	if (isLoaded())
  224  		return true;
  225  
  226  	// Don't load images greater than screen resolution
  227  	MaxSizeInfo maxSize(Renderer::getScreenWidth(), Renderer::getScreenHeight(), false);
  228  	if (!mMaxSize.empty() && mMaxSize.x() < maxSize.x() && mMaxSize.y() < maxSize.y())
  229  		maxSize = mMaxSize;
  230  		
  231  	auto oldSize = mSize;
  232  
  233  	size_t width, height;
  234  	Vector2i size;
  235  	Vector2i physicalSize;
  236  	unsigned char* imageRGBA = ImageIO::loadFromMemoryRGBA32((const unsigned char*)(fileData), length, width, height, &maxSize, &physicalSize, &size, subImageIndex);
  237  	
  238  	mPhysicalSize = Vector2f(physicalSize.x(), physicalSize.y());
  239  	mSize = size.empty() ? physicalSize : size;
  240  	mScalable = false;
  241  
  242  	if (imageRGBA == nullptr)
  243  	{
  244  		LOG(LogError) << "Could not initialize texture from memory, invalid data!  (file path: " << mPath << ", data ptr: " << (size_t)fileData << ", reported size: " << length << ")";
  245  		return false;
  246  	}
  247  
  248  	return initFromRGBA(imageRGBA, width, height, false);
  249  }
  250  
  251  bool TextureData::initFromRGBA(unsigned char* dataRGBA, size_t width, size_t height, bool copyData)
  252  {
  253  	// If already initialised then don't read again
  254  	std::unique_lock<std::mutex> lock(mMutex);
  255  
  256  	if (mIsExternalDataRGBA)
  257  	{
  258  		mIsExternalDataRGBA = false;
  259  		mDataRGBA = nullptr;
  260  	}
  261  
  262  	if (mDataRGBA)
  263  		return true;
  264  
  265  	if (copyData)
  266  	{
  267  		// Take a copy
  268  		mDataRGBA = new unsigned char[width * height * 4];
  269  		memcpy(mDataRGBA, dataRGBA, width * height * 4);
  270  	}
  271  	else
  272  		mDataRGBA = dataRGBA;
  273  
  274  	mSize = Vector2i(width, height);
  275  
  276  	if (copyData)
  277  		mPhysicalSize = Vector2f(mSize.x(), mSize.y());
  278  
  279  	return true;
  280  }
  281  
  282  bool TextureData::updateFromExternalRGBA(unsigned char* dataRGBA, size_t width, size_t height)
  283  {
  284  	std::unique_lock<std::mutex> lock(mMutex);
  285  
  286  	if (!mIsExternalDataRGBA && mDataRGBA != nullptr)
  287  		delete[] mDataRGBA;
  288  
  289  #if defined(USE_OPENGLES_30)
  290  	const bool dimensionsChanged = mSize.x() != static_cast<int>(width) || mSize.y() != static_cast<int>(height);
  291  #endif
  292  
  293  	mIsExternalDataRGBA = true;
  294  	mDataRGBA = dataRGBA;
  295  	mSize = Vector2i(width, height);
  296  	mPhysicalSize = Vector2f(width, height);
  297  
  298  	if (mTextureID != 0)
  299  	{
  300  #if defined(USE_OPENGLES_30)
  301  		if (dimensionsChanged || mMipmapped)
  302  		{
  303  			Renderer::destroyTexture(mTextureID);
  304  			mTextureID = Renderer::createTexture(Renderer::Texture::RGBA, mLinear, mTile, width, height, mDataRGBA);
  305  			mMipmapped = false;
  306  		}
  307  		else
  308  #endif
  309  			Renderer::updateTexture(mTextureID, Renderer::Texture::RGBA, 0, 0, width, height, mDataRGBA);
  310  	}
  311  
  312  	return true;
  313  }
  314  
  315  // Avoid multiple extraction in the same file at the same time
  316  static Utils::StringListLockType mImageExtractorLock;
  317  
  318  #if WIN32
  319  extern void _checkUpgradedVlcVersion();
  320  #endif
  321  
  322  bool TextureData::loadFromVideo()
  323  {
  324  	Utils::StringListLock lock(mImageExtractorLock, mPath);
  325  
  326  	auto val = Utils::FileSystem::createRelativePath(Utils::FileSystem::changeExtension(mPath, ".jpg"), Paths::getHomePath(), true);
  327  	val = Utils::String::replace(val, "~/../", "./");
  328  
  329  	std::string localFile = Utils::FileSystem::resolveRelativePath(val, Paths::getUserEmulationStationPath() + "/tmp/videothumbs/", true);
  330  
  331  	if (Utils::FileSystem::exists(localFile))
  332  	{
  333  		auto date = Utils::FileSystem::getFileCreationDate(localFile);
  334  		auto duration = Utils::Time::DateTime::now().elapsedSecondsSince(date);
  335  		if (duration > 62 * 86400) // 2 months
  336  			Utils::FileSystem::removeFile(localFile);
  337  	}
  338  
  339  	if (!Utils::FileSystem::exists(localFile))
  340  	{
  341  		Utils::FileSystem::createDirectory(Utils::FileSystem::getParent(localFile));
  342  
  343  		libvlc_instance_t *vlcInstance = nullptr;
  344  		libvlc_media_t *vlcMedia = nullptr;
  345  		libvlc_media_player_t *vlcMediaPlayer = nullptr;
  346  
  347  		std::vector<std::string> cmdline;
  348  		cmdline.push_back("--quiet");
  349  		cmdline.push_back("--rate=1");
  350  		cmdline.push_back("--video-filter=scene");
  351  		cmdline.push_back("--intf=dummy");
  352  		cmdline.push_back("--vout=dummy");
  353  		cmdline.push_back("--scene-format=jpeg");
  354  		cmdline.push_back("--scene-ratio=1");
  355  		cmdline.push_back("--no-video-title-show");
  356  
  357  		const char** vlcArgs = new const char*[cmdline.size()];
  358  
  359  		for (int i = 0; i < cmdline.size(); i++)
  360  			vlcArgs[i] = cmdline[i].c_str();
  361  
  362  #if WIN32
  363  		_checkUpgradedVlcVersion();
  364  #endif
  365  
  366  		vlcInstance = libvlc_new(cmdline.size(), vlcArgs);
  367  		if (vlcInstance == nullptr)
  368  			return false;
  369  
  370  		vlcMedia = libvlc_media_new_path(vlcInstance, Utils::FileSystem::getPreferredPath(mPath).c_str());
  371  		if (vlcMedia == nullptr)
  372  		{
  373  			libvlc_release(vlcInstance);
  374  			return false;
  375  		}
  376  
  377  		libvlc_media_add_option(vlcMedia, ":no-audio");
  378  		libvlc_media_add_option(vlcMedia, ":start-time=1.5");
  379  
  380  		vlcMediaPlayer = libvlc_media_player_new_from_media(vlcMedia);
  381  		if (vlcMediaPlayer == nullptr)
  382  		{
  383  			libvlc_media_release(vlcMedia);
  384  			libvlc_release(vlcInstance);
  385  			return false;
  386  		}
  387  
  388  		int ms = 1500;
  389  
  390  		libvlc_media_player_set_rate(vlcMediaPlayer, 1);
  391  		libvlc_audio_set_mute(vlcMediaPlayer, 1);
  392  		libvlc_media_player_play(vlcMediaPlayer);
  393  		libvlc_media_player_set_time(vlcMediaPlayer, ms);
  394  
  395  		auto time = libvlc_media_player_get_time(vlcMediaPlayer);
  396  		int n = 100; // avoid infinite loop
  397  		while (time <= ms && n > 0) {
  398  			time = libvlc_media_player_get_time(vlcMediaPlayer);
  399  			n--;
  400  		}
  401  
  402  		int result = libvlc_video_take_snapshot(vlcMediaPlayer, 0, localFile.c_str(), 0, 0);
  403  
  404  		libvlc_media_player_stop(vlcMediaPlayer);
  405  		libvlc_media_player_release(vlcMediaPlayer);
  406  		libvlc_media_release(vlcMedia);
  407  		libvlc_release(vlcInstance);
  408  	}
  409  
  410  	if (Utils::FileSystem::exists(localFile))
  411  	{
  412  		std::shared_ptr<ResourceManager>& rm = ResourceManager::getInstance();
  413  		const ResourceData& data = rm->getFileData(localFile);
  414  		return initImageFromMemory((const unsigned char*)data.ptr.get(), data.length);
  415  	}
  416  
  417  	return false;
  418  }
  419  
  420  bool TextureData::loadFromPdf(int pageIndex)
  421  {
  422  	if (PdfHandler == nullptr)
  423  		return false;
  424  	
  425  	bool retval = false;
  426  
  427  	Utils::StringListLock lock(mImageExtractorLock, mPath);
  428  	
  429  	int dpi = 48;
  430  
  431  	if (!mMaxSize.empty())
  432  		dpi = (int) Math::clamp(mMaxSize.y() / 6, 32, 300);
  433  
  434  	auto files = PdfHandler->extractPdfImages(mPath, pageIndex, pageIndex, dpi);
  435  	if (files.size() > 0)
  436  	{
  437  		std::shared_ptr<ResourceManager>& rm = ResourceManager::getInstance();
  438  		const ResourceData& data = rm->getFileData(files[0]);
  439  		Utils::FileSystem::removeFile(files[0]);
  440  
  441  		initImageFromMemory((const unsigned char*)data.ptr.get(), data.length);
  442  	}
  443  
  444  	return retval;
  445  }
  446  
  447  bool TextureData::loadFromCbz()
  448  {
  449  	bool retval = false;
  450  
  451  	Utils::StringListLock lock(mImageExtractorLock, mPath);
  452  
  453  	std::vector<Utils::Zip::ZipInfo> files;
  454  
  455  	Utils::Zip::ZipFile zipFile;
  456  	if (zipFile.load(mPath))
  457  	{
  458  		for (auto file : zipFile.infolist())
  459  		{
  460  			auto ext = Utils::String::toLower(Utils::FileSystem::getExtension(file.filename));
  461  			if (ext != ".jpg")
  462  				continue;
  463  
  464  			if (Utils::String::startsWith(file.filename, "__"))
  465  				continue;
  466  
  467  			files.push_back(file);
  468  		}
  469  
  470  		std::sort(files.begin(), files.end(), [](const Utils::Zip::ZipInfo& a, const Utils::Zip::ZipInfo& b) { return Utils::String::toLower(a.filename) < Utils::String::toLower(b.filename); });
  471  	}
  472  
  473  	if (files.size() > 0 && files[0].file_size > 0)
  474  	{
  475  		size_t size = files[0].file_size;
  476  		unsigned char* buffer = new unsigned char[size];
  477  
  478  		Utils::Zip::zip_callback func = [](void *pOpaque, uint64_t ofs, const void *pBuf, size_t n)
  479  		{
  480  			unsigned char* pSource = (unsigned char*)pBuf;
  481  			unsigned char* pDest = (unsigned char*)pOpaque;
  482  
  483  			memcpy(pDest + ofs, pSource, n);
  484  
  485  			return n;
  486  		};
  487  
  488  		zipFile.readBuffered(files[0].filename, func, buffer);		
  489  		retval = initImageFromMemory(buffer, size);
  490  	}
  491  
  492  	return retval;
  493  }
  494  
  495  bool TextureData::load()
  496  {
  497  	// Need to load. See if there is a file
  498  	if (mPath.empty())
  499  		return false;
  500  
  501  	LOG(LogDebug) << "TextureData::load " << mPath;
  502  	mScalable = false;
  503  
  504  	std::string ext = Utils::String::toLower(Utils::FileSystem::getExtension(mPath));
  505  
  506  	if (ext == ".cbz")
  507  		return loadFromCbz();
  508  
  509  	if (ext == ".pdf")
  510  		return PdfHandler != nullptr ? loadFromPdf() : false;
  511  
  512  	if (Utils::FileSystem::isVideo(mPath))
  513  		return loadFromVideo();
  514  
  515  	std::string path = mPath;
  516  	int subImageIndex = -1;
  517  
  518  	if (ext.find(',') != std::string::npos)
  519  	{
  520  		auto idx = path.rfind(',');
  521  		subImageIndex = Utils::String::toInteger(mPath.substr(idx + 1));
  522  		path = mPath.substr(0, idx);
  523  	}
  524  
  525  	const ResourceData& data = ResourceManager::getInstance()->getFileData(path);
  526  	if (data.length == 0)
  527  		return false;
  528  
  529  	// is it an SVG?
  530  	if (ext == ".svg")
  531  	{
  532  		mScalable = true;
  533  		return initSVGFromMemory((const unsigned char*)data.ptr.get(), data.length);
  534  	}
  535  
  536  	return initImageFromMemory((const unsigned char*)data.ptr.get(), data.length, subImageIndex);
  537  }
  538  
  539  bool TextureData::isLoaded()
  540  {
  541  	std::unique_lock<std::mutex> lock(mMutex);
  542  	if (mDataRGBA || (mTextureID != 0))
  543  		return true;
  544  
  545  	return false;
  546  }
  547  
  548  bool TextureData::uploadAndBind()
  549  {
  550  	// See if it's already been uploaded
  551  	std::unique_lock<std::mutex> lock(mMutex);
  552  
  553  	if (mTextureID != 0)
  554  		Renderer::bindTexture(mTextureID);
  555  	else
  556  	{
  557  		// Make sure we're ready to upload
  558  		if (mSize.empty() || mDataRGBA == nullptr)
  559  		{
  560  			Renderer::bindTexture(mTextureID);
  561  			return false;
  562  		}
  563  
  564  #if defined(USE_OPENGLES_30)
  565  		// Mipmaps reduce 4K artwork minification cost and aliasing, but add about 33%
  566  		// VRAM. Restrict them to stable, path-backed linear artwork that will not be
  567  		// updated every frame (video/external pixels, fonts, and render targets never enter here).
  568  		const bool useMipmaps = mReloadable && !mIsExternalDataRGBA && mLinear && !mTile &&
  569  			!Utils::FileSystem::isVideo(mPath) && (mSize.x() >= 256 || mSize.y() >= 256);
  570  		mTextureID = useMipmaps
  571  			? Renderer::createMipmappedTexture(Renderer::Texture::RGBA, mLinear, mTile, mSize.x(), mSize.y(), mDataRGBA)
  572  			: Renderer::createTexture(Renderer::Texture::RGBA, mLinear, mTile, mSize.x(), mSize.y(), mDataRGBA);
  573  #else
  574  		// Legacy renderers retain their original single-level texture path.
  575  		mTextureID = Renderer::createTexture(Renderer::Texture::RGBA, mLinear, mTile, mSize.x(), mSize.y(), mDataRGBA);
  576  #endif
  577  		if (mTextureID == 0)
  578  			return false;
  579  #if defined(USE_OPENGLES_30)
  580  		mMipmapped = useMipmaps;
  581  #endif
  582  
  583  		if (mDataRGBA != nullptr && !mIsExternalDataRGBA)
  584  			delete[] mDataRGBA;
  585  
  586  		mDataRGBA = nullptr;
  587  	}
  588  
  589  	return true;
  590  }
  591  
  592  void TextureData::releaseVRAM()
  593  {
  594  	std::unique_lock<std::mutex> lock(mMutex);
  595  	if (mTextureID != 0)
  596  	{
  597  		Renderer::destroyTexture(mTextureID);
  598  		mTextureID = 0;
  599  #if defined(USE_OPENGLES_30)
  600  		mMipmapped = false;
  601  #endif
  602  	}
  603  }
  604  
  605  void TextureData::releaseRAM()
  606  {
  607  	std::unique_lock<std::mutex> lock(mMutex);
  608  
  609  	if (mDataRGBA != nullptr && !mIsExternalDataRGBA)
  610  		delete[] mDataRGBA;
  611  
  612  	mDataRGBA = 0;
  613  }
  614  
  615  void TextureData::setMaxSize(const MaxSizeInfo& maxSize)
  616  {
  617  	if (!OPTIMIZEVRAM)
  618  		return;
  619  
  620  	if (mPhysicalSize.empty())
  621  	{
  622  		// Not loaded yet. A shared texture gets here once per consumer, in whatever
  623  		// order they ask, and the first load honours whatever is left in mMaxSize.
  624  		// For an SVG that box decides the raster, so a later, smaller consumer must
  625  		// not shrink it: keep the larger box per axis, and the first raster fits the
  626  		// largest request while the smaller consumers downsample (#181). Bitmaps and
  627  		// tiles keep the old replace: a bitmap's box is only a cap, which rasterizeAt
  628  		// already grows on demand, and a tile's bitmap size is its pitch.
  629  		if (mMaxSize.empty() || mTile || !Utils::FileSystem::isSVG(mPath))
  630  			mMaxSize = maxSize;
  631  		else if (maxSize.x() > mMaxSize.x() || maxSize.y() > mMaxSize.y())
  632  			mMaxSize = MaxSizeInfo(Math::max(mMaxSize.x(), maxSize.x()), Math::max(mMaxSize.y(), maxSize.y()),
  633  				mMaxSize.externalZoom() || maxSize.externalZoom());
  634  	}
  635  	else
  636  	{
  637  		auto imageSize = Vector2i((int)Math::round(mPhysicalSize.x()), Math::round(mPhysicalSize.y()));
  638  
  639  		Vector2i value = ImageIO::adjustPictureSize(imageSize, Vector2i(mMaxSize.x(), mMaxSize.y()), mMaxSize.externalZoom());
  640  		Vector2i newVal = ImageIO::adjustPictureSize(imageSize, Vector2i(maxSize.x(), maxSize.y()), mMaxSize.externalZoom());
  641  
  642  		if (newVal.x() > value.x() || newVal.y() > value.y())
  643  			mMaxSize = maxSize;
  644  	}
  645  }
  646  
  647  bool TextureData::isMaxSizeValid()
  648  {
  649  	if (!OPTIMIZEVRAM)
  650  		return true;
  651  
  652  	if (mSize.empty() || mPhysicalSize.empty())
  653  		return true;
  654  
  655  	if (mMaxSize.empty())
  656  		return true;
  657  
  658  	if ((int) Math::round(mPhysicalSize.x()) == mSize.x() && (int)Math::round(mPhysicalSize.y()) == mSize.y())
  659  		return true;
  660  
  661  	if ((int)mMaxSize.x() <= mSize.x() || (int)mMaxSize.y() <= mSize.y())
  662  		return true;
  663  
  664  	if (mPhysicalSize.x() <= mSize.x() || mPhysicalSize.y() <= mSize.y())
  665  		return true;
  666  
  667  	return false;
  668  }
  669  
  670  bool TextureData::rasterizeAt(float width, float height)
  671  {
  672  	if (mSize.empty())
  673  		return false;
  674  
  675  	int h = (int)Math::round(height);
  676  	int w = (int)Math::round(width);
  677  
  678  	if (mScalable)
  679  	{
  680  		if ((int)Math::round(mScalableMinimumSize.y()) < h && (int)Math::round(mScalableMinimumSize.x()) != w)
  681  		{
  682  			LOG(LogDebug) << "Requested SVG image size too small. Reloading image from (" << mScalableMinimumSize.x() << ", " << mScalableMinimumSize.y() << ") to (" << width << ", " << height << ")";
  683  
  684  			mScalableMinimumSize.x() = width;
  685  			mScalableMinimumSize.y() = height;
  686  
  687  			if (!mTile && !mMaxSize.empty() && !mPhysicalSize.empty())
  688  			{
  689  				// The reload rasterises at this height and then clamps to mMaxSize,
  690  				// which still holds the box of whichever consumer loaded the texture
  691  				// first. Grow it to the request, never shrink it, as the bitmap
  692  				// branch below already does, so the clamp cannot undo the reload
  693  				// (#181). The raster takes its width from the source aspect, not
  694  				// from the request, so make room for that width too: mPhysicalSize
  695  				// is the last raster, an integer bitmap whose true aspect is within
  696  				// half a pixel of x/y. Without it a consumer sized freely by the
  697  				// theme ("size" rather than "maxSize") could see the clamp trim a
  698  				// pixel and ask again at every layout.
  699  				float fitW = Math::round(h * (mPhysicalSize.x() + 0.5f) / mPhysicalSize.y()) + 1.0f;
  700  				float needW = Math::max((float)w, fitW);
  701  
  702  				if (mMaxSize.x() < needW || mMaxSize.y() < h)
  703  				{
  704  					LOG(LogDebug) << "Growing SVG max size from (" << mMaxSize.x() << ", " << mMaxSize.y() << ") to fit (" << width << ", " << height << ")";
  705  					mMaxSize = MaxSizeInfo(Math::max(mMaxSize.x(), needW), Math::max(mMaxSize.y(), (float)h), mMaxSize.externalZoom());
  706  				}
  707  			}
  708  
  709  			if (!isLoaded())
  710  				return true;
  711  
  712  			releaseVRAM();
  713  			releaseRAM();
  714  			load();
  715  
  716  			return isLoaded();
  717  		}
  718  	}
  719  	else if (!mMaxSize.empty() && h < Renderer::getScreenHeight() && w < Renderer::getScreenWidth() && OPTIMIZEVRAM)
  720  	{
  721  		if (mSize.y() < h && mSize.x() < w && (int)Math::round(mPhysicalSize.y()) >= h && (int)Math::round(mPhysicalSize.x()) > w)
  722  		{
  723  			LOG(LogDebug) << "Requested PNG/JPG image size too small. Reloading image from (" << mSize.x() << ", " << mSize.y() << ") to (" << width << ", " << height << ")";
  724  
  725  			mMaxSize = MaxSizeInfo(w, h, mMaxSize.externalZoom());
  726  
  727  			if (!isLoaded())
  728  				return true;
  729  
  730  			releaseVRAM();
  731  			releaseRAM();
  732  			load();
  733  
  734  			return isLoaded();
  735  		}
  736  	}
  737  
  738  	return false;
  739  }
```

## src/resources/TextureDataManager.cpp `:127-178` (an excerpt, upstream-carried, at the pin)

```text
  127  	bool isResource = first->getPath().rfind(":/") == 0;
  128  	bool secondIsResource = second->getPath().rfind(":/") == 0;
  129  	if (isResource && !secondIsResource)
  130  		return true;
  131  
  132  	return (second->isRequired() && !first->isRequired());
  133  }
  134  
  135  void TextureDataManager::cleanupVRAM()
  136  {
  137  	std::unique_lock<std::recursive_mutex> lock(mMutex);
  138  
  139  	size_t maxVRAM = (size_t)Settings::getInstance()->getInt("MaxVRAM") * 1024 * 1024;
  140  	size_t size = TextureResource::getTotalMemoryUsage(MemoryUsageType::Allocated);
  141  
  142  	if (size < maxVRAM)
  143  		return;
  144  
  145  	// Perform cleanup on textures
  146  	for (auto it = mTextures.crbegin(); it != mTextures.crend(); ++it)
  147  	{
  148  		auto tex = *it;
  149  		if (!tex->isReloadable() || tex->isRequired() || !tex->isLoaded())
  150  			continue;
  151  
  152  		auto textureSize = tex->getMemoryUsage(MemoryUsageType::Allocated); // pass == 0 ? MemoryUsageType::RAM : MemoryUsageType::VRAM);
  153  		if (textureSize == 0)
  154  			continue;
  155  
  156  		LOG(LogDebug) << "Cleanup VRAM\tReleased : " << tex->getPath().c_str() << ", " << std::to_string(tex->getSize().x()) << "x" << std::to_string(tex->getSize().y());
  157  
  158  		tex->releaseVRAM();
  159  		tex->releaseRAM();
  160  
  161  		size -= textureSize;
  162  		if (size <= maxVRAM)
  163  			break;
  164  	}
  165  
  166  	// On x86 platforms, perform cleanup on textures stored in RAM, limit to 250Mb
  167  	if (sizeof(void*) == 4)
  168  	{
  169  		size_t maxRAM = 250 * 1024 * 1024;
  170  		size = TextureResource::getTotalMemoryUsage(MemoryUsageType::RAM);
  171  
  172  		if (size > maxRAM)
  173  		{
  174  			for (auto it = mTextures.crbegin(); it != mTextures.crend(); ++it)
  175  			{
  176  				auto tex = *it;
  177  				if (!tex->isReloadable() || tex->isRequired() || !tex->isLoaded())
  178  					continue;
```

## src/resources/TextureDataManager.cpp `:207-261` (an excerpt, upstream-carried, at the pin)

```text
  207  	mLoader->remove(tex);	
  208  
  209  	if (!block)
  210  		mLoader->load(tex);
  211  	else
  212  		tex->load();	
  213  }
  214  
  215  TextureLoader::TextureLoader(TextureDataManager* mgr) : mManager(mgr), mExit(false)
  216  {
  217  	int num_threads = std::thread::hardware_concurrency() / 2;
  218  	if (num_threads < 2)
  219  		num_threads = 2;
  220  
  221  	for (size_t i = 0; i < num_threads; i++)
  222  		mThreads.push_back(std::thread(&TextureLoader::threadProc, this));
  223  }
  224  
  225  TextureLoader::~TextureLoader()
  226  {
  227  	// Just abort any waiting texture
  228  	clearQueue();
  229  
  230  	// Exit the thread
  231  	mExit = true;
  232  	mEvent.notify_all();
  233  
  234  	for (std::thread& t : mThreads)
  235  		t.join();
  236  }
  237  
  238  #if WIN32
  239  #include <Windows.h>
  240  #endif
  241  
  242  void TextureLoader::threadProc()
  243  {
  244  #if WIN32
  245  	if (Utils::Platform::isWindows10())
  246  		SetThreadDescription(GetCurrentThread(), L"TextureLoader::threadProc");
  247  #endif
  248  
  249  	while (true)
  250  	{		
  251  		// Wait for an event to say there is something in the queue
  252  		std::unique_lock<std::mutex> lock(mLoaderLock);
  253  		mEvent.wait(lock, [this]() { return !paused && (mExit || !mTextureDataQ.empty()); });
  254  
  255  		if (mExit)
  256  			break;
  257  
  258  		if (!mTextureDataQ.empty())
  259  		{
  260  			std::shared_ptr<TextureData> textureData = mTextureDataQ.front();
  261  
```

## src/resources/TextureDataManager.cpp `:276-292` (an excerpt, upstream-carried, at the pin)

```text
  276  				mProcessingTextureDataQ.erase(textureData);
  277  			}
  278  
  279  			lock.unlock();			
  280  		}		
  281  	}
  282  }
  283  
  284  std::atomic<bool> TextureLoader::paused = false;
  285  
  286  void TextureLoader::load(std::shared_ptr<TextureData> textureData)
  287  {
  288  //	if (paused)
  289  	//	return;
  290  
  291  	std::unique_lock<std::mutex> lock(mLoaderLock);
  292  
```

## src/resources/TextureResource.cpp `:4-20` (an excerpt, upstream-carried, at the pin)

```text
    4  #include "resources/TextureData.h"
    5  #include <cstring>
    6  #include "Settings.h"
    7  #include "PowerSaver.h"
    8  #include "Log.h"
    9  #include "renderers/Renderer.h"
   10  
   11  TextureDataManager		TextureResource::sTextureDataManager;
   12  std::map< TextureResource::TextureKeyType, std::weak_ptr<TextureResource> > TextureResource::sTextureMap;
   13  std::set<TextureResource*> 	TextureResource::sNonDynamicTextureResources;
   14  
   15  TextureResource::TextureResource(const std::string& path, bool tile, bool linear, bool dynamic, bool allowAsync, const MaxSizeInfo* maxSize) : mTextureData(nullptr), mForceLoad(false)
   16  {
   17  	// Create a texture data object for this texture
   18  	if (!path.empty())
   19  	{
   20  		// If there is a path then the 'dynamic' flag tells us whether to use the texture
```

## src/resources/TextureResource.cpp `:68-173` (an excerpt, upstream-carried, at the pin)

```text
   68  			sNonDynamicTextureResources.erase(pthis);
   69  	}
   70  }
   71  
   72  void TextureResource::cleanupTextureResourceCache()
   73  {
   74  	std::vector<TextureKeyType> toRemove;
   75  
   76  	for (auto item : sTextureMap)
   77  		if (item.second.expired())
   78  			toRemove.push_back(item.first);
   79  
   80  	for (auto tmp : toRemove)
   81  		sTextureMap.erase(tmp);
   82  }
   83  
   84  std::shared_ptr<TextureResource> TextureResource::get(const std::string& path, bool tile, bool linear, bool forceLoad, bool dynamic, bool asReloadable, const MaxSizeInfo* maxSize, const std::string& shareId)
   85  {
   86  	std::shared_ptr<ResourceManager>& rm = ResourceManager::getInstance();
   87  
   88  	const std::string canonicalPath = Utils::FileSystem::getCanonicalPath(path);
   89  	if (canonicalPath.empty())
   90  	{
   91  		std::shared_ptr<TextureResource> tex = std::make_shared<TextureResource>("", tile, linear, false, false);
   92  		rm->addReloadable(tex); //make sure we get properly deinitialized even though we do nothing on reinitialization
   93  		return tex;
   94  	}
   95  
   96  	// internal resources should not be dynamic
   97  	if (canonicalPath.length() > 0 && canonicalPath[0] == ':')
   98  		dynamic = false;
   99  
  100  	TextureKeyType key(canonicalPath, tile, linear, shareId);
  101  
  102  	//TextureKeyType key(canonicalPath, tile, linear);
  103  	auto foundTexture = sTextureMap.find(key);
  104  	if (foundTexture != sTextureMap.cend())
  105  	{
  106  		if (!foundTexture->second.expired())
  107  		{
  108  			std::shared_ptr<TextureResource> rc = foundTexture->second.lock();
  109  
  110  			if (maxSize != nullptr && !maxSize->empty() && Settings::getInstance()->getBool("OptimizeVRAM"))
  111  			{
  112  				std::shared_ptr<TextureData> dt;
  113  				if (rc->mTextureData != nullptr)
  114  					dt = rc->mTextureData;
  115  				else
  116  					dt = sTextureDataManager.get(rc.get(), TextureLoadMode::NOLOAD);
  117  
  118  				if (dt != nullptr)
  119  				{
  120  					dt->setMaxSize(*maxSize);
  121  
  122  					if (dt->isLoaded() && !dt->isMaxSizeValid())
  123  					{
  124  						dt->releaseVRAM();
  125  						dt->releaseRAM();
  126  						dt->load();
  127  					}
  128  				}
  129  			}
  130  
  131  			return rc;
  132  		}
  133  		else if (!asReloadable)
  134  			sTextureMap.erase(foundTexture);
  135  	}
  136  
  137  	// need to create it
  138  	std::shared_ptr<TextureResource> tex;
  139  	tex = std::make_shared<TextureResource>(std::get<0>(key), tile, linear, dynamic, !forceLoad, maxSize);
  140  
  141  	auto loadMode = forceLoad ? TextureLoadMode::STANDARD: TextureLoadMode::NOLOAD;
  142  	std::shared_ptr<TextureData> data = sTextureDataManager.get(tex.get(), loadMode);
  143  
  144  	if (asReloadable)
  145  	{
  146  		sTextureMap[key] = std::weak_ptr<TextureResource>(tex);
  147  
  148  		// Add it to the reloadable list
  149  		rm->addReloadable(tex);
  150  	}
  151  
  152  	if (data != nullptr && maxSize != nullptr)
  153  		data->setMaxSize(*maxSize);
  154  
  155  	// Force load it if necessary. Note that it may get dumped from VRAM if we run low
  156  	if (forceLoad)
  157  	{
  158  		tex->mForceLoad = forceLoad;
  159  
  160  		if (data != nullptr && !data->isLoaded())
  161  			data->load();
  162  	}
  163  
  164  	return tex;
  165  }
  166  
  167  void TextureResource::updateFromExternalPixels(unsigned char* dataRGBA, size_t width, size_t height)
  168  {
  169  	// This is only valid if we have a local texture data object
  170  	if (mTextureData == nullptr)
  171  		return;
  172  
  173  	mTextureData->updateFromExternalRGBA(dataRGBA, width, height);
```

## src/utils/CommandLineUtil.h (whole, fork-added, at the pin)

```text
    1  #pragma once
    2  #ifndef ES_CORE_UTILS_COMMAND_LINE_UTIL_H
    3  #define ES_CORE_UTILS_COMMAND_LINE_UTIL_H
    4  
    5  #include <string>
    6  
    7  // A launch command's option, replaced in place (the save state manager's
    8  // "this state was made with another core": SaveState::setupSaveState).
    9  // Header-only and pure, so es-unit-tests reaches it without SaveState's
   10  // FileData and SystemConf (es-app/tests/unit/CommandLineTests.cpp).
   11  namespace Utils
   12  {
   13  	namespace CommandLine
   14  	{
   15  		// Where each shell word of `line` starts and ends, outside quotes:
   16  		// single quotes take everything to the next one, double quotes and a
   17  		// bare word honour a backslash, and unquoted whitespace ends a word.
   18  		// An unterminated quote runs to the end of the line.
   19  		inline size_t wordEnd(const std::string& line, size_t pos)
   20  		{
   21  			char quote = 0;
   22  			for (size_t i = pos; i < line.size(); i++)
   23  			{
   24  				const char c = line[i];
   25  				if (quote == '\'')
   26  				{
   27  					if (c == '\'')
   28  						quote = 0;
   29  					continue;
   30  				}
   31  				if (c == '\\')
   32  				{
   33  					i++;   // the next character, whatever it is
   34  					continue;
   35  				}
   36  				if (quote == '"')
   37  				{
   38  					if (c == '"')
   39  						quote = 0;
   40  					continue;
   41  				}
   42  				if (c == '\'' || c == '"')
   43  					quote = c;
   44  				else if (c == ' ' || c == '\t')
   45  					return i;
   46  			}
   47  			return line.size();
   48  		}
   49  
   50  		// `line` with the value of the option `parameter` ("-core",
   51  		// "-emulator") replaced by `value`. ROCKNIX passes it joined --
   52  		// --core=<v> -- and the legacy launchers separate, -core <v>; either
   53  		// is found only as a whole word of the command, never inside a quoted
   54  		// argument such as the ROM's path (#308 F-CS-33: the joined form was
   55  		// the last "--core=" anywhere in the line, its value ending at the
   56  		// next literal space, so a ROM name spelling the same letters after
   57  		// the real option was rewritten and could lose its closing quote).
   58  		// The joined form's last word wins, as before; the separate form's
   59  		// first. A line with neither comes back as it was.
   60  		inline std::string replaceOptionValue(const std::string& line, const std::string& parameter, const std::string& value)
   61  		{
   62  			const std::string joined = "-" + parameter + "=";   // "-core" -> "--core="
   63  
   64  			size_t joinedAt = std::string::npos;
   65  			size_t separateAt = std::string::npos, separateValue = std::string::npos, separateEnd = std::string::npos;
   66  			size_t i = 0;
   67  			while (i < line.size())
   68  			{
   69  				if (line[i] == ' ' || line[i] == '\t')
   70  				{
   71  					i++;
   72  					continue;
   73  				}
   74  				const size_t end = wordEnd(line, i);
   75  				if (line.compare(i, joined.size(), joined) == 0)
   76  					joinedAt = i;
   77  				else if (separateAt == std::string::npos && end - i == parameter.size() && line.compare(i, parameter.size(), parameter) == 0)
   78  				{
   79  					size_t v = end;
   80  					while (v < line.size() && (line[v] == ' ' || line[v] == '\t'))
   81  						v++;
   82  					if (v < line.size())
   83  					{
   84  						separateAt = i;
   85  						separateValue = v;
   86  						separateEnd = wordEnd(line, v);
   87  					}
   88  				}
   89  				i = end;
   90  			}
   91  
   92  			if (joinedAt != std::string::npos)
   93  			{
   94  				const size_t from = joinedAt + joined.size();
   95  				return line.substr(0, from) + value + line.substr(wordEnd(line, joinedAt));
   96  			}
   97  			if (separateAt != std::string::npos)
   98  				return line.substr(0, separateValue) + value + line.substr(separateEnd);
   99  			return line;
  100  		}
  101  	}
  102  }
  103  
  104  #endif // ES_CORE_UTILS_COMMAND_LINE_UTIL_H
```

## src/utils/FileSystemUtil.cpp `:30-372` (an excerpt, upstream-carried, at the pin)

```text
   30  #else // _WIN32
   31  #include <dirent.h>
   32  #include <unistd.h>
   33  #include <mutex>
   34  #endif // _WIN32
   35  
   36  #include <fstream>
   37  #include <sstream>
   38  #include <unordered_map>
   39  #include <optional>
   40  #include <climits>
   41  
   42  #include "Paths.h"
   43  
   44  namespace Utils
   45  {
   46  	namespace FileSystem
   47  	{		
   48  		struct FileCache
   49  		{
   50  			FileCache() 
   51  			{
   52  				_directory = false;
   53  				_exists = false;
   54  				_hidden = false;
   55  				_symlink = false;
   56  			}
   57  
   58  			FileCache(bool exists, bool dir, bool symLink = false)
   59  			{
   60  				_directory = dir;
   61  				_exists = exists;
   62  				_hidden = false;
   63  				_symlink = symLink;
   64  			}
   65  
   66  #if WIN32			
   67  			FileCache(DWORD dwFileAttributes)
   68  			{
   69  				if (0xFFFFFFFF == dwFileAttributes)
   70  				{
   71  					_directory = false;
   72  					_exists = false;
   73  					_hidden = false;
   74  					_symlink = false;
   75  				}
   76  				else
   77  				{
   78  					_exists = true;
   79  					_directory = dwFileAttributes & FILE_ATTRIBUTE_DIRECTORY;
   80  					_hidden = dwFileAttributes & FILE_ATTRIBUTE_HIDDEN;
   81  					_symlink = dwFileAttributes & FILE_ATTRIBUTE_REPARSE_POINT;
   82  				}
   83  			}			
   84  			
   85  			FileCache(WIN32_FIND_DATAW& data)
   86  			{
   87  				_exists = true;
   88  				_directory = data.dwFileAttributes & FILE_ATTRIBUTE_DIRECTORY;
   89  				_hidden = data.dwFileAttributes & FILE_ATTRIBUTE_HIDDEN;
   90  				_symlink = data.dwFileAttributes & FILE_ATTRIBUTE_REPARSE_POINT;
   91  			}
   92  
   93  			static void add(const std::string& key, WIN32_FIND_DATAW& data)
   94  			{
   95  				if (!Settings::UseFileCache())
   96  					return;
   97  
   98  				std::unique_lock<std::shared_mutex> guard(mFileCacheMutex);
   99  
  100  				auto [it, inserted] = mFileCache.try_emplace(hashPath(key), data);
  101  				if (!inserted)
  102  				{
  103  					it->second._exists = true;
  104  					it->second._directory = data.dwFileAttributes & FILE_ATTRIBUTE_DIRECTORY;
  105  					it->second._hidden = data.dwFileAttributes & FILE_ATTRIBUTE_HIDDEN;
  106  					it->second._symlink = data.dwFileAttributes & FILE_ATTRIBUTE_REPARSE_POINT;
  107  				}
  108  			}
  109  
  110  			static void add(const std::string& key, DWORD dwFileAttributes)
  111  			{
  112  				if (!Settings::UseFileCache())
  113  					return;
  114  
  115  				std::unique_lock<std::shared_mutex> guard(mFileCacheMutex);
  116  
  117  				auto [it, inserted] = mFileCache.try_emplace(hashPath(key), dwFileAttributes); 
  118  				if (!inserted)
  119  				{
  120  					if (0xFFFFFFFF == dwFileAttributes)
  121  					{
  122  						it->second._directory = false;
  123  						it->second._exists = false;
  124  						it->second._hidden = false;
  125  						it->second._symlink = false;
  126  					}
  127  					else
  128  					{
  129  						it->second._exists = true;
  130  						it->second._directory = dwFileAttributes & FILE_ATTRIBUTE_DIRECTORY;
  131  						it->second._hidden = dwFileAttributes & FILE_ATTRIBUTE_HIDDEN;
  132  						it->second._symlink = dwFileAttributes & FILE_ATTRIBUTE_REPARSE_POINT;
  133  					}					
  134  				}
  135  			}
  136  #endif
  137  
  138  			static int fromStat64(const std::string& key, struct stat64* info)
  139  			{
  140  #if WIN32			
  141  				int ret = _wstat64(Utils::String::convertToWideString(key).c_str(), info);
  142  
  143  				std::unique_lock<std::shared_mutex> guard(mFileCacheMutex);
  144  				mFileCache.try_emplace(hashPath(key), ret == 0, ret == 0 && S_ISDIR(info->st_mode));				
  145  #else
  146  				int ret = stat64(key.c_str(), info);
  147  
  148  				FileCache cache(ret == 0, false);
  149  				if (cache._exists)
  150  				{
  151  					cache._directory = S_ISDIR(info->st_mode);
  152  					cache._symlink = S_ISLNK(info->st_mode);
  153  					if (cache._symlink)
  154  					{
  155  						struct stat64 si;
  156  						if (stat64(resolveSymlink(key).c_str(), &si) == 0)
  157  							cache._directory = S_ISDIR(si.st_mode);
  158  					}
  159  				}
  160  
  161  				std::unique_lock<std::shared_mutex> guard(mFileCacheMutex);
  162  				mFileCache[hashPath(key)] = cache;			
  163  #endif
  164  
  165  				return ret;
  166  			}
  167  
  168  			static void add(const std::string& key, bool exists, bool dir, bool symlink = false)
  169  			{
  170  				if (!Settings::UseFileCache())
  171  					return;
  172  
  173  				std::unique_lock<std::shared_mutex> guard(mFileCacheMutex);
  174  				auto [it, inserted] = mFileCache.try_emplace(hashPath(key), exists, dir, symlink);
  175  				if (!inserted)
  176  				{
  177  					it->second._exists = exists;
  178  					it->second._directory = dir;
  179  					it->second._symlink = symlink;
  180  				}
  181  			}
  182  
  183  			static void remove(const std::string& key)
  184  			{
  185  				if (!Settings::UseFileCache())
  186  					return;
  187  
  188  				std::unique_lock<std::shared_mutex> guard(mFileCacheMutex);
  189  
  190  				mFileCache.erase(hashPath(key));
  191  				
  192  				auto parent = Utils::FileSystem::getParent(key);
  193  				while (!parent.empty())
  194  				{
  195  					mFileCache.erase(hashPath(parent + "/*"));
  196  					parent = Utils::FileSystem::getParent(parent);
  197  				}
  198  			}
  199  
  200  			template<typename Func>
  201  			static std::optional<bool> queryCacheEntry(const std::string& key, Func func)
  202  			{
  203  				if (!Settings::UseFileCache())
  204  					return std::nullopt;
  205  
  206  				auto hash = hashPath(key);
  207  				{
  208  					std::shared_lock<std::shared_mutex> lock(mFileCacheMutex);
  209  					if (auto* e = getCacheEntry(key, hash))
  210  						return func(e);
  211  				}
  212  
  213  				auto fetched = statKey(key);
  214  				std::unique_lock<std::shared_mutex> lock(mFileCacheMutex);
  215  				return func(&insertEntry(hash, key, std::move(fetched)));
  216  			}
  217  
  218  			static std::optional<bool> exists(const std::string& key)
  219  			{
  220  				return queryCacheEntry(key, [](const FileCache* e) { return std::optional<bool>(e->_exists); });
  221  			}
  222  
  223  			// Non-blocking probe: returns true if the key's existence is already
  224  			// recorded in the cache (either exists or known-not-to-exist).
  225  			// Never calls stat64 — safe to call from the render thread.
  226  			static bool isCached(const std::string& key)
  227  			{
  228  				if (!Settings::UseFileCache())
  229  					return false;
  230  
  231  				auto hash = hashPath(key);
  232  				std::shared_lock<std::shared_mutex> lock(mFileCacheMutex);
  233  				if (mFileCache.count(hash))
  234  					return true;
  235  				return mFileCache.count(hashPath(Utils::FileSystem::getParent(key) + "/*")) > 0;
  236  			}
  237  
  238  			static std::optional<bool> isRegularFile(const std::string& key)
  239  			{
  240  				return queryCacheEntry(key, [](const FileCache* e) { return std::optional<bool>(e->_exists && !e->_directory && !e->_symlink); });
  241  			}
  242  
  243  			static std::optional<bool> isDirectory(const std::string& key)
  244  			{
  245  				return queryCacheEntry(key, [](const FileCache* e) { return std::optional<bool>(e->_exists && e->_directory); });
  246  			}
  247  
  248  			static std::optional<bool> isSymlink(const std::string& key)
  249  			{
  250  				return queryCacheEntry(key, [](const FileCache* e) { return std::optional<bool>(e->_exists && e->_symlink); });
  251  			}
  252  
  253  			static std::optional<bool> isHidden(const std::string& key)
  254  			{
  255  				return queryCacheEntry(key, [&key](const FileCache* e) { return std::optional<bool>(e->_exists && (e->_hidden || getFileName(key)[0] == '.')); });
  256  			}
  257  
  258  			static void resetCache()
  259  			{
  260  				std::unique_lock<std::shared_mutex> guard(mFileCacheMutex);
  261  				mFileCache.clear();
  262  			}
  263  
  264  		private:
  265  			// Looks up key in the cache. MUST be called under at least a shared_lock.
  266  			// Returns pointer to the entry if found (including parent-wildcard hits,
  267  			// which return a static "not exists" sentinel), or nullptr if not cached.
  268  			static const FileCache* getCacheEntry(const std::string& key, size_t hash)
  269  			{
  270  				if (mFileCache.empty())
  271  					return nullptr;
  272  
  273  				auto it = mFileCache.find(hash);
  274  				if (it != mFileCache.cend())
  275  					return &it->second;
  276  
  277  				it = mFileCache.find(hashPath(Utils::FileSystem::getParent(key) + "/*"));
  278  				if (it != mFileCache.cend())
  279  				{
  280  					static const FileCache notExists(false, false);
  281  					return &notExists;
  282  				}
  283  
  284  				return nullptr;
  285  			}
  286  
  287  			// Performs filesystem I/O with NO lock held — safe to call concurrently.
  288  			static FileCache statKey(const std::string& key)
  289  			{
  290  #ifdef WIN32
  291  				return FileCache(GetFileAttributesW(Utils::String::convertToWideString(key).c_str()));
  292  #else
  293  				struct stat64 info;
  294  				int ret = stat64(key.c_str(), &info);
  295  
  296  				bool exists = ret == 0;
  297  				bool directory = exists && S_ISDIR(info.st_mode);
  298  				bool symlink = exists && S_ISLNK(info.st_mode);
  299  				if (symlink)
  300  				{
  301  					struct stat64 si;
  302  					if (stat64(resolveSymlink(key).c_str(), &si) == 0)
  303  						directory = S_ISDIR(si.st_mode);
  304  				}
  305  
  306  				return FileCache(exists, directory, symlink);
  307  #endif
  308  			}
  309  
  310  			// Inserts a pre-computed entry. MUST be called with exclusive lock held.
  311  			// Double-checks for races: returns the authoritative entry (ours or a
  312  			// concurrent thread's insert, whichever arrived first).
  313  			static const FileCache& insertEntry(size_t hash, const std::string& key, FileCache fetched)
  314  			{
  315  				auto it = mFileCache.find(hash);
  316  				if (it != mFileCache.cend())
  317  					return it->second;
  318  
  319  				it = mFileCache.find(hashPath(Utils::FileSystem::getParent(key) + "/*"));
  320  				if (it != mFileCache.cend())
  321  					return mFileCache.try_emplace(hash, false, false).first->second;
  322  
  323  				return mFileCache.try_emplace(hash, std::move(fetched)).first->second;
  324  			}
  325  
  326  			bool _exists;
  327  			bool _directory;
  328  			bool _hidden;
  329  			bool _symlink;
  330  
  331  			static std::unordered_map<size_t, FileCache> mFileCache;
  332  			static std::shared_mutex mFileCacheMutex;
  333  
  334  			static size_t hashPath(const std::string& path) 
  335  			{ 
  336  				return std::hash<std::string>{}(getGenericPath(path));
  337  			}
  338  		};
  339  
  340  		std::unordered_map<size_t, FileCache> FileCache::mFileCache;
  341  		std::shared_mutex FileCache::mFileCacheMutex;
  342  
  343  		void FileSystemCache::reset()
  344  		{
  345  			FileCache::resetCache();
  346  		}
  347  
  348  		void FileSystemCache::reset(const std::string& file)
  349  		{
  350  			FileCache::remove(file);
  351  		}
  352  
  353  	// Methods
  354  
  355  		stringList getDirContent(const std::string& _path, const bool _recursive, const bool includeHidden)
  356  		{
  357  			std::string path = getGenericPath(_path);
  358  			stringList  contentList;
  359  
  360  			// only parse the directory, if it's a directory
  361  			if(isDirectory(path))
  362  			{
  363  				// tell filecache we enumerated the folder
  364  				FileCache::add(path + "/*", true, true);
  365  
  366  #if defined(_WIN32)
  367  				WIN32_FIND_DATAW findData;
  368  				std::string      wildcard = path + "/*";
  369  				
  370  				HANDLE hFind = FindFirstFileExW(Utils::String::convertToWideString(wildcard).c_str(),
  371  					FINDEX_INFO_LEVELS::FindExInfoBasic, &findData, FINDEX_SEARCH_OPS::FindExSearchNameMatch
  372  					, NULL, FIND_FIRST_EX_LARGE_FETCH);
```

## src/utils/FileSystemUtil.cpp `:425-441` (an excerpt, upstream-carried, at the pin)

```text
  425  								if (stat64(resolveSymlink(fullName).c_str(), &info) == 0)
  426  									directory = S_ISDIR(info.st_mode);
  427  								else
  428  									directory = false;
  429  							}
  430  							else
  431  								directory = (entry->d_type == 4);
  432  
  433  							FileCache::add(fullName, true, directory, entry->d_type == 10);
  434  
  435  							if (!includeHidden && hidden)
  436  								continue;
  437  
  438  							contentList.push_back(fullName);
  439  
  440  							if (_recursive && directory)
  441  							{
```

## src/utils/FileSystemUtil.cpp `:471-487` (an excerpt, upstream-carried, at the pin)

```text
  471  #endif
  472  
  473  		fileList getDirectoryFiles(const std::string& _path)
  474  		{
  475  			std::string path = getGenericPath(_path);
  476  			fileList  contentList;
  477  
  478  			// tell filecache we enumerated the folder
  479  			FileCache::add(path + "/*", true, true);
  480  
  481  			// only parse the directory, if it's a directory
  482  			// if (isDirectory(path))
  483  			{			
  484  #if defined(_WIN32)
  485  
  486  				if (_path.empty() || _path == "\\" || _path == "/")
  487  				{
```

## src/utils/FileSystemUtil.cpp `:567-583` (an excerpt, upstream-carried, at the pin)

```text
  567  								if (stat64(resolveSymlink(fullName).c_str(), &si) == 0)
  568  									fi.directory = S_ISDIR(si.st_mode);
  569  								else
  570  									fi.directory = false;
  571  							}
  572  							else
  573  								fi.directory = (entry->d_type == 4); // DT_DIR;
  574  
  575  							FileCache::add(fullName, true, fi.directory, entry->d_type == 10);
  576  
  577  							//DT_LNK
  578  							contentList.push_back(fi);
  579  						}
  580  					}
  581  
  582  					closedir(dir);
  583  				}
```

## src/utils/FileSystemUtil.cpp `:1043-1209` (an excerpt, upstream-carried, at the pin)

```text
 1043  		bool removeDirectory(const std::string& _path)
 1044  		{
 1045  			std::string path = getGenericPath(_path);
 1046  
 1047  			// don't remove if it doesn't exists
 1048  			if (!exists(path, false))
 1049  				return true;
 1050  
 1051  			FileCache::remove(path);
 1052  #if WIN32			
 1053  			return RemoveDirectoryW(Utils::String::convertToWideString(getPreferredPath(_path)).c_str());
 1054  #else
 1055  			return (rmdir(path.c_str()) == 0);
 1056  #endif
 1057  		}
 1058  
 1059  		bool removeFile(const std::string& _path)
 1060  		{
 1061  			std::string path = getGenericPath(_path);
 1062  
 1063  			// don't remove if it doesn't exists
 1064  			if (!exists(path, false))
 1065  				return true;
 1066  
 1067  			FileCache::remove(path);
 1068  #if WIN32			
 1069  			if (isDirectory(_path))
 1070  				return RemoveDirectoryW(Utils::String::convertToWideString(getPreferredPath(_path)).c_str());
 1071  						
 1072  			if (!DeleteFileW(Utils::String::convertToWideString(_path).c_str()))
 1073  			{
 1074  				SetFileAttributesW(Utils::String::convertToWideString(_path).c_str(), FILE_ATTRIBUTE_NORMAL);
 1075  				return DeleteFileW(Utils::String::convertToWideString(_path).c_str());
 1076  			}
 1077  
 1078  			return true;
 1079  #else
 1080  			if (isDirectory(_path))
 1081  				return (rmdir(path.c_str()) == 0);
 1082  
 1083  			// try to remove file
 1084  			return (unlink(path.c_str()) == 0);
 1085  #endif
 1086  
 1087  		} // removeFile
 1088  
 1089  		bool createDirectory(const std::string& _path)
 1090  		{
 1091  			std::string path = getGenericPath(_path);
 1092  
 1093  			// don't create if it already exists
 1094  			if (exists(path, false))
 1095  				return true;
 1096  
 1097  			FileCache::remove(path);
 1098  
 1099  #ifdef WIN32	
 1100  			if (::CreateDirectoryW(Utils::String::convertToWideString(_path).c_str(), nullptr))
 1101  				return true;
 1102  #endif
 1103  
 1104  			// try to create directory
 1105  			if (mkdir(path.c_str(), 0755) == 0)
 1106  				return true;
 1107  
 1108  			// failed to create directory, try to create the parent
 1109  			std::string parent = getParent(path);
 1110  
 1111  			// only try to create parent if it's not identical to path
 1112  			if (parent != path)
 1113  				createDirectory(parent);
 1114  						
 1115  			// try to create directory again now that the parent should exist
 1116  			if (mkdir(path.c_str(), 0755) == 0)
 1117  				return true;
 1118  
 1119  			return false;
 1120  		} // createDirectory
 1121  
 1122  		bool exists(const std::string& _path, bool enableCache)
 1123  		{
 1124  			if (_path.empty())
 1125  				return false;
 1126  
 1127  			if (enableCache)
 1128  			{
 1129  				auto val = FileCache::exists(_path);
 1130  				if (val)
 1131  					return *val;
 1132  			}
 1133  
 1134  #ifdef WIN32			
 1135  			DWORD dwAttr = GetFileAttributesW(Utils::String::convertToWideString(_path).c_str());
 1136  			FileCache::add(_path, dwAttr);
 1137  			if (0xFFFFFFFF == dwAttr)
 1138  				return false;
 1139  
 1140  			return true;
 1141  #else
 1142  			std::string path = getGenericPath(_path);
 1143  			struct stat64 info;
 1144  
 1145  			return FileCache::fromStat64(path, &info) == 0;
 1146  #endif
 1147  		} // exists
 1148  
 1149  		bool isAbsolute(const std::string& _path)
 1150  		{
 1151  			if(_path.size() >= 2 && _path[0] == ':' && _path[1] == '/')
 1152  				return true;
 1153  		
 1154  			std::string path = getGenericPath(_path);
 1155  
 1156  #ifdef WIN32
 1157  			return ((path.size() > 1) && (path[1] == ':'));
 1158  #else // _WIN32
 1159  			return ((path.size() > 0) && (path[0] == '/'));
 1160  #endif // _WIN32
 1161  
 1162  		} // isAbsolute
 1163  
 1164  		bool isRegularFile(const std::string& _path)
 1165  		{
 1166  			auto it = FileCache::isRegularFile(_path);
 1167  			if (it) return *it;
 1168  
 1169  			std::string path = getGenericPath(_path);
 1170  			struct stat64 info;
 1171  
 1172  			// check if stat64 succeeded
 1173  			if (FileCache::fromStat64(path, &info) != 0) //if(stat64(path.c_str(), &info) != 0)				
 1174  				return false;
 1175  
 1176  			// check for S_IFREG attribute
 1177  			return (S_ISREG(info.st_mode));
 1178  
 1179  		} // isRegularFile
 1180  
 1181  		bool isDirectory(const std::string& _path)
 1182  		{
 1183  			auto it = FileCache::isDirectory(_path);
 1184  			if (it) return *it;
 1185  
 1186  #ifdef WIN32
 1187  			// check for symlink attribute
 1188  			DWORD dwAttributes = GetFileAttributesW(Utils::String::convertToWideString(_path).c_str());
 1189  			FileCache::add(_path, dwAttributes);
 1190  			return (dwAttributes != INVALID_FILE_ATTRIBUTES) && (dwAttributes & FILE_ATTRIBUTE_DIRECTORY);
 1191  #else // _WIN32
 1192  			std::string path = getGenericPath(_path);
 1193  			struct stat64 info;
 1194  
 1195  			// check if stat succeeded
 1196  			if (FileCache::fromStat64(path, &info) != 0) //if(stat64(path.c_str(), &info) != 0)
 1197  				return false;
 1198  
 1199  			if (S_ISLNK(info.st_mode))
 1200  			{
 1201  				if (FileCache::fromStat64(resolveSymlink(path), &info) != 0) //if(stat64(path.c_str(), &info) != 0)
 1202  					return false;
 1203  			}
 1204  
 1205  			// check for S_IFDIR attribute
 1206  			return (S_ISDIR(info.st_mode));
 1207  #endif
 1208  		} // isDirectory
 1209  
```

## src/utils/FileSystemUtil.cpp `:1222-1238` (an excerpt, upstream-carried, at the pin)

```text
 1222  				return true;
 1223  
 1224  			// not a symlink
 1225  			return false;
 1226  #else // WIN32
 1227  			struct stat64 info;
 1228  
 1229  			// check if lstat succeeded
 1230  			if (FileCache::fromStat64(path, &info) != 0) //if(stat64(path.c_str(), &info) != 0)			
 1231  				return false;
 1232  
 1233  			// check for S_IFLNK attribute
 1234  			return (S_ISLNK(info.st_mode));
 1235  #endif //_WIN32
 1236  			
 1237  		} // isSymlink
 1238  
```

## src/utils/FileSystemUtil.cpp `:1361-1387` (an excerpt, upstream-carried, at the pin)

```text
 1361  				return Utils::Time::DateTime(info.st_mtime);
 1362  #else
 1363  			if ((stat64(path.c_str(), &info) == 0))
 1364  				return Utils::Time::DateTime(info.st_mtime);
 1365  #endif
 1366  			return Utils::Time::DateTime();
 1367  		}
 1368  
 1369  		static void skipUtf8Bom(std::ifstream& file) 
 1370  		{
 1371  			if (!file.is_open())
 1372  				return;
 1373  
 1374  			char bom[3];
 1375  			if (file.read(bom, 3) && bom[0] == '\xEF' && bom[1] == '\xBB' && bom[2] == '\xBF')			
 1376  				return;
 1377  			
 1378  			file.seekg(0);
 1379  		}
 1380  
 1381  		std::vector<char> readAllBytes(const std::string& fileName)
 1382  		{
 1383  			std::ifstream file(WINSTRINGW(fileName), std::ios::binary | std::ios::ate);
 1384  			if (!file.is_open())
 1385  				return {};
 1386  
 1387  			std::streampos size = file.tellg();			
```

## src/utils/FileSystemUtil.cpp `:1392-1539` (an excerpt, upstream-carried, at the pin)

```text
 1392  			
 1393  			std::vector<char> buffer(size);			
 1394  			if (!file.read(buffer.data(), size))
 1395  				return {};
 1396  
 1397  			return buffer;
 1398  		}
 1399  
 1400  		std::list<std::string> readAllLines(const std::string& fileName)
 1401  		{
 1402  			std::list<std::string> lines;
 1403  
 1404  			std::ifstream file(WINSTRINGW(fileName));
 1405  			if (!file.is_open()) 
 1406  				return lines;
 1407  
 1408  			skipUtf8Bom(file);
 1409  
 1410  			std::string line;
 1411  			while (std::getline(file, line))
 1412  				lines.push_back(line);
 1413  
 1414  			file.close();
 1415  			return lines;
 1416  		}
 1417  
 1418  		std::string	readAllText(const std::string& fileName)
 1419  		{
 1420  			std::ifstream t(WINSTRINGW(fileName));
 1421  
 1422  			skipUtf8Bom(t);
 1423  
 1424  			std::stringstream buffer;
 1425  			buffer << t.rdbuf();
 1426  			return buffer.str();
 1427  		}
 1428  
 1429  		void writeAllText(const std::string& fileName, const std::string& text)
 1430  		{
 1431  #if defined(_WIN32)
 1432  			FILE* file = _wfopen(Utils::String::convertToWideString(fileName).c_str(), L"wb");
 1433  #else
 1434  			FILE* file = fopen(fileName.c_str(), "wb");
 1435  #endif
 1436  			if (file == nullptr)
 1437  				return;		
 1438  
 1439  			void* buffer = (void*) text.data();
 1440  			size_t size = text.size();
 1441  
 1442  			fwrite(buffer, 1, size, file);
 1443  			fclose(file);
 1444  
 1445  			FileCache::remove(getGenericPath(fileName));
 1446  		}
 1447  
 1448  		bool renameFile(const std::string& src, const std::string& dst, bool overWrite)
 1449  		{
 1450  			std::string path = getGenericPath(src);			
 1451  			if (!exists(path, false))
 1452  				return true;
 1453  
 1454  			if (overWrite && exists(dst, false))
 1455  				removeFile(dst);
 1456  
 1457  			FileCache::remove(path);
 1458  			FileCache::remove(dst);
 1459  
 1460  #if WIN32			
 1461  			return MoveFileW(Utils::String::convertToWideString(path).c_str(), Utils::String::convertToWideString(dst).c_str());
 1462  #else
 1463  			return std::rename(src.c_str(), dst.c_str()) == 0;
 1464  #endif
 1465  		}
 1466  
 1467  		bool copyFile(const std::string& src, const std::string& dst)
 1468  		{
 1469  			std::string path = getGenericPath(src);
 1470  			std::string pathD = getGenericPath(dst);
 1471  
 1472  			// don't remove if it doesn't exists
 1473  			if (!exists(path, false))
 1474  				return true;
 1475  
 1476  			Utils::FileSystem::createDirectory(Utils::FileSystem::getParent(pathD));
 1477  
 1478  			char buf[512];
 1479  			size_t size;
 1480  
 1481  #if defined(_WIN32)
 1482  			FILE* source = _wfopen(Utils::String::convertToWideString(path).c_str(), L"rb");
 1483  #else
 1484  			FILE* source = fopen(path.c_str(), "rb");
 1485  #endif
 1486  			if (source == nullptr)
 1487  				return false;
 1488  
 1489  #if defined(_WIN32)
 1490  			FILE* dest = _wfopen(Utils::String::convertToWideString(pathD).c_str(), L"wb");
 1491  #else
 1492  			FILE* dest = fopen(pathD.c_str(), "wb");
 1493  #endif
 1494  			if (dest == nullptr)
 1495  			{
 1496  				fclose(source);
 1497  				return false;
 1498  			}
 1499  
 1500  			while (size = fread(buf, 1, 512, source))
 1501  				fwrite(buf, 1, size, dest);
 1502  
 1503  			fclose(dest);
 1504  			fclose(source);
 1505  
 1506  			FileCache::remove(path);
 1507  			FileCache::remove(pathD);
 1508  
 1509  			return true;
 1510  		} // removeFile
 1511  
 1512  		void deleteDirectoryFiles(const std::string& path, bool deleteDirectory)
 1513  		{
 1514  			std::vector<std::string> directories;
 1515  
 1516  			auto files = Utils::FileSystem::getDirContent(path, true, true);
 1517  			std::reverse(std::begin(files), std::end(files));
 1518  			for (auto file : files)
 1519  			{
 1520  				if (Utils::FileSystem::isDirectory(file))
 1521  					directories.push_back(file);
 1522  				else
 1523  					Utils::FileSystem::removeFile(file);
 1524  			}
 1525  
 1526  			for (auto file : directories)
 1527  				removeDirectory(file);
 1528  
 1529  			if (deleteDirectory)
 1530  				removeDirectory(path);
 1531  		}
 1532  
 1533  		std::string megaBytesToString(unsigned long size)
 1534  		{
 1535  			static const char *SIZES[] = { "MB", "GB", "TB" };
 1536  			int div = 0;
 1537  			unsigned long rem = 0;
 1538  
 1539  			while (size >= 1024 && div < (sizeof SIZES / sizeof *SIZES))
```

## src/utils/FileSystemUtil.cpp `:1750-1805` (an excerpt, upstream-carried, at the pin)

```text
 1750  				else
 1751  				{
 1752  					*executable = c.substr(0, exec_end);
 1753  					std::string().swap(*parameters);
 1754  				}
 1755  			}
 1756  		}
 1757  #endif
 1758  		void preloadFileSystemCache(const std::string& path, bool trySaveStates)
 1759  		{
 1760  			if (path.empty())
 1761  				return;
 1762  
 1763  			if (!Settings::UseFileCache())
 1764  				return;
 1765  
 1766  			static std::set<std::string> preloaded;
 1767  
 1768  			if (preloaded.find(path) != preloaded.cend())
 1769  				return;
 1770  
 1771  			preloaded.insert(path);
 1772  
 1773  			auto doWork = [&](std::string* dir)
 1774  			{
 1775  				if (trySaveStates)
 1776  				{
 1777  					std::string systemName = Utils::FileSystem::getFileName(*dir);
 1778  					Utils::FileSystem::getDirContent(Utils::FileSystem::combine(Paths::getSavesPath(), systemName), true);
 1779  				}
 1780  
 1781  				Utils::FileSystem::getDirContent(Utils::FileSystem::combine(*dir, "/images"));
 1782  				Utils::FileSystem::getDirContent(Utils::FileSystem::combine(*dir, "/videos"));
 1783  				Utils::FileSystem::getDirContent(Utils::FileSystem::combine(*dir, "/manuals"));
 1784  
 1785  				delete dir;
 1786  			};
 1787  
 1788  			std::thread thread(doWork, new std::string(path));
 1789  
 1790  #if WIN32		
 1791  			if (Utils::Platform::isWindows10())
 1792  				::SetThreadDescription(thread.native_handle(), L"PreloadFileSystemCache");
 1793  
 1794  			::SetThreadPriority(thread.native_handle(), THREAD_PRIORITY_LOWEST);
 1795  #endif
 1796  
 1797  			thread.detach();
 1798  		}
 1799  
 1800  	} // FileSystem::
 1801  
 1802  } // Utils::
 1803  
 1804  
 1805  
```

## src/utils/MathExpr.cpp `:87-103` (an excerpt, upstream-carried, at the pin)

```text
   87  		// Math
   88  		{ { "min", 2 },           [](const Args& args) { return std::to_string(Math::min(Utils::String::toFloat(removeStringQuotes(args[0])), Utils::String::toFloat(removeStringQuotes(args[1])))); } },
   89  		{ { "max", 2 },           [](const Args& args) { return std::to_string(Math::max(Utils::String::toFloat(removeStringQuotes(args[0])), Utils::String::toFloat(removeStringQuotes(args[1])))); } },
   90  		{ { "clamp", 3 },         [](const Args& args) { return std::to_string(Math::clamp( Utils::String::toFloat(removeStringQuotes(args[0])),  Utils::String::toFloat(removeStringQuotes(args[1])), Utils::String::toFloat(removeStringQuotes(args[2])) )); } },
   91  		{ { "tostring", 1 },      [](const Args& args) { return addStringQuotes(args[0]); } },
   92  
   93  		// Misc
   94  		{ { "default", 1 },       [](const Args& args) { auto dataAsString = removeStringQuotes(args[0]);
   95  														 return addStringQuotes(dataAsString.empty() ? _("Unknown") : dataAsString == "0" ? _("None") : dataAsString); } },
   96  		{ { "year", 1 },          [](const Args& args) { auto time = Utils::Time::stringToTime(removeStringQuotes(args[0]), "%Y%m%d");
   97  														 return addStringQuotes(time <= 0 ? "" : Utils::Time::timeToString(time, "%Y")); } },
   98  		{ { "month", 1 },         [](const Args& args) { auto time = Utils::Time::stringToTime(removeStringQuotes(args[0]), "%Y%m%d");
   99  														 return addStringQuotes(time <= 0 ? "" : Utils::Time::timeToString(time, "%m")); } },
  100  		{ { "day", 1 },           [](const Args& args) { auto time = Utils::Time::stringToTime(removeStringQuotes(args[0]), "%Y%m%d");
  101  														 return addStringQuotes(time <= 0 ? "" : Utils::Time::timeToString(time, "%d")); } },
  102  		{ { "elapsed", 1 },       [](const Args& args) { auto time = Utils::Time::stringToTime(removeStringQuotes(args[0]), "%Y%m%dT%H%M%S");
  103  														 return addStringQuotes(time <= 0 ? "" : Utils::Time::getElapsedSinceString(time)); } },
```

## src/utils/OfflineProxyUrl.cpp (whole, fork-added, at the pin)

```text
    1  #include "utils/OfflineProxyUrl.h"
    2  
    3  #include <cctype>
    4  #include <cstring>
    5  
    6  bool Utils::OfflineProxy::isProxyUrl(const std::string& url)
    7  {
    8  	const size_t baseLength = std::strlen(Base);
    9  	if (url.size() < baseLength)
   10  		return false;
   11  
   12  	for (size_t i = 0; i < baseLength; i++)
   13  		if (std::tolower((unsigned char)url[i]) != std::tolower((unsigned char)Base[i]))
   14  			return false;
   15  
   16  	if (url.size() == baseLength)
   17  		return true;
   18  
   19  	const char next = url[baseLength];
   20  	return next == '/' || next == '?' || next == '#';
   21  }
```

## src/utils/OfflineProxyUrl.h (whole, fork-added, at the pin)

```text
    1  #pragma once
    2  #ifndef ES_CORE_UTILS_OFFLINE_PROXY_URL_H
    3  #define ES_CORE_UTILS_OFFLINE_PROXY_URL_H
    4  
    5  #include <string>
    6  
    7  // The offline RetroAchievements proxy's address on this device, and the one
    8  // question the interface asks of a URL: is this the proxy? (fork #199)
    9  //
   10  // Pure: a string and a rule about it, so es-app/tests/unit can hold it to
   11  // its word. The proxy is RAOfflineProxy on the loopback, at the port
   12  // setsettings.sh points RetroArch at for every launch. OfflineAchievementsText
   13  // builds the pages' requests on Base; WebImageComponent asks isProxyUrl before
   14  // it fetches an image, because a request to the proxy carries a header no
   15  // other host is sent. One definition, so the two cannot drift apart.
   16  namespace Utils
   17  {
   18  	namespace OfflineProxy
   19  	{
   20  		// Scheme, host and port, no trailing slash: what every request to
   21  		// the proxy is built on.
   22  		const char* const Base = "http://127.0.0.1:8080";
   23  
   24  		// The request header that asks the proxy for its store and nothing
   25  		// else (the fork's proxy patches 010 and 012): a dorequest.php
   26  		// answer from the store whatever the proxy believes about the link,
   27  		// an image it holds or a 404 at once. As HttpReqOptions::customHeaders
   28  		// takes it, name and value in one line.
   29  		const char* const StoreOnlyHeader = "X-RA-Store-Only: 1";
   30  
   31  		// Whether url is a request to the proxy: Base, compared without
   32  		// regard to case (a scheme and a host are case-insensitive), followed
   33  		// by the end of the string, a path, a query or a fragment -- so a host
   34  		// that merely begins with it (127.0.0.1:80800, 127.0.0.1:8080.example)
   35  		// is not, and neither is https, another port, or no port.
   36  		bool isProxyUrl(const std::string& url);
   37  	}
   38  }
   39  
   40  #endif // ES_CORE_UTILS_OFFLINE_PROXY_URL_H
```

## src/utils/Platform.cpp (whole, fork-modified, at the pin)

```text
    1  #include "Platform.h"
    2  
    3  #include <SDL_events.h>
    4  
    5  #if WIN32
    6  #include <codecvt>
    7  #include <windows.h>
    8  #else
    9  #include <sys/types.h>
   10  #include <unistd.h>
   11  #include <ifaddrs.h>
   12  #include <net/if.h>
   13  #include <netinet/in.h>
   14  #include <sys/stat.h>
   15  #include <arpa/inet.h>
   16  #include <sys/wait.h>
   17  #include <unistd.h>
   18  #endif
   19  
   20  #include <fcntl.h>
   21  #include "Window.h"
   22  #include "utils/FileSystemUtil.h"
   23  #include "utils/StringUtil.h"
   24  #include "Log.h"
   25  #include "Scripting.h"
   26  #include "Paths.h"
   27  #include <fstream>
   28  #include <string>
   29  #include "renderers/Renderer.h"
   30  
   31  // #define DEVTEST
   32  
   33  namespace Utils
   34  {
   35  	namespace Platform
   36  	{
   37  		ProcessStartInfo::ProcessStartInfo()
   38  		{
   39  			window = nullptr;
   40  			waitForExit = true;
   41  			showWindow = true;
   42  #ifndef WIN32
   43  			stderrFilename = "es_launch_stderr.log";
   44  			stdoutFilename = "es_launch_stdout.log";
   45  #endif
   46  		}
   47  
   48  		ProcessStartInfo::ProcessStartInfo(const std::string& cmd)
   49  		{
   50  			command = cmd;
   51  			window = nullptr;
   52  			waitForExit = true;
   53  			showWindow = true;
   54  #ifndef WIN32
   55  			stderrFilename = "es_launch_stderr.log";
   56  			stdoutFilename = "es_launch_stdout.log";
   57  #endif
   58  		}
   59  
   60  		int ProcessStartInfo::run() const
   61  		{
   62  			if (command.empty())
   63  				return 1;
   64  
   65  			if (window != nullptr)
   66  				window->renderSplashScreen();
   67  
   68  			std::string cmd_utf8 = command;
   69  
   70  #ifdef WIN32
   71  			std::wstring cmd_w = Utils::String::convertToWideString(cmd_utf8);
   72  
   73  			DWORD dwLen = ExpandEnvironmentStringsW(cmd_w.c_str(), NULL, 0);
   74  			if (dwLen > 0)
   75  			{
   76  				WCHAR* szEnvPath = new WCHAR[dwLen];
   77  
   78  				dwLen = ExpandEnvironmentStringsW(cmd_w.c_str(), szEnvPath, dwLen);
   79  				if (dwLen > 0)
   80  					cmd_utf8 = Utils::String::convertFromWideString(szEnvPath);
   81  
   82  				delete[] szEnvPath;
   83  			}
   84  
   85  			std::string exe;
   86  			std::string args;
   87  			Utils::FileSystem::splitCommand(cmd_utf8, &exe, &args);
   88  
   89  			exe = Utils::FileSystem::getPreferredPath(exe);
   90  
   91  			std::wstring wexe = Utils::String::convertToWideString(exe);
   92  			std::wstring wargs = Utils::String::convertToWideString(args);
   93  
   94  			SHELLEXECUTEINFOW lpExecInfo;
   95  			lpExecInfo.cbSize = sizeof(SHELLEXECUTEINFOW);
   96  			lpExecInfo.lpFile = wexe.c_str();
   97  			lpExecInfo.fMask = SEE_MASK_DOENVSUBST | SEE_MASK_NOCLOSEPROCESS;
   98  			lpExecInfo.hwnd = NULL;
   99  			lpExecInfo.lpVerb = L"open"; // to open  program
  100  			lpExecInfo.lpDirectory = NULL;
  101  			lpExecInfo.nShow = showWindow ? SW_SHOW : SW_HIDE;  // show command prompt with normal window size
  102  			lpExecInfo.hInstApp = (HINSTANCE)SE_ERR_DDEFAIL;   //WINSHELLAPI BOOL WINAPI result;
  103  			lpExecInfo.lpParameters = wargs.c_str(); //  file name as an argument
  104  
  105  			std::wstring wpath;
  106  
  107  			// Don't set directory for relative paths
  108  			if (!Utils::String::startsWith(exe, ".") && !Utils::String::startsWith(exe, "/") && !Utils::String::startsWith(exe, "\\"))
  109  			{
  110  				wpath = Utils::String::convertToWideString(Utils::FileSystem::getAbsolutePath(Utils::FileSystem::getParent(exe)));
  111  				lpExecInfo.lpDirectory = wpath.c_str();
  112  			}
  113  
  114  			if (waitForExit)
  115  				Renderer::setWindowResizable(false);
  116  
  117  			ShellExecuteExW(&lpExecInfo);
  118  
  119  			if (lpExecInfo.hProcess != NULL)
  120  			{
  121  				if (!waitForExit)
  122  					return 0;
  123  
  124  				if (window == nullptr)
  125  					WaitForSingleObject(lpExecInfo.hProcess, INFINITE);
  126  				else
  127  				{
  128  				
  129  
  130  					while (WaitForSingleObject(lpExecInfo.hProcess, 50) == 0x00000102L)
  131  					{
  132  						bool polled = false;
  133  
  134  						SDL_Event event;
  135  						while (SDL_PollEvent(&event))
  136  							polled = true;
  137  
  138  						if (window != nullptr && polled)
  139  							window->renderSplashScreen();
  140  					}				
  141  				}
  142  
  143  				DWORD dwExitCode;
  144  				if (!GetExitCodeProcess(lpExecInfo.hProcess, &dwExitCode))
  145  					dwExitCode = 0;
  146  
  147  				CloseHandle(lpExecInfo.hProcess); 
  148  				
  149  				if (waitForExit)
  150  					Renderer::setWindowResizable(true);
  151  
  152  				return dwExitCode;
  153  			}
  154  
  155  			if (waitForExit)
  156  				Renderer::setWindowResizable(true);
  157  
  158  			return 1;
  159  #else
  160  			// getting the output when in a pipe is not easy...
  161  			// https://stackoverflow.com/questions/1221833/pipe-output-and-capture-exit-status-in-bash
  162  			std::string cmdOutput = "((((" + cmd_utf8 + " 2> " + Utils::FileSystem::combine(Paths::getLogPath(), stderrFilename) + " ; echo $? >&3) | head -300 > " + Utils::FileSystem::combine(Paths::getLogPath(), stdoutFilename) + ") 3>&1) | (read xs; exit $xs))";
  163  			if (!Log::enabled())
  164  			  cmdOutput = "((((" + cmd_utf8 + " 2> /dev/null ; echo $? >&3) | head -300 > /dev/null) 3>&1) | (read xs; exit $xs))";
  165  
  166  			if (waitForExit) {
  167  			  int n = system(cmdOutput.c_str());
  168  			  return WEXITSTATUS(n);
  169  			}
  170  
  171  			// fork the current process
  172  			pid_t ret = fork();
  173  			if (ret == 0)
  174  			{
  175  				ret = fork();
  176  				if (ret == 0)
  177  				{
  178  					execl("/bin/sh", "sh", "-c", cmdOutput.c_str(), (char *) NULL);
  179  					_exit(1); // execl failed
  180  				}
  181  				_exit(0); // exit the child process
  182  			}
  183  			else
  184  			{
  185  				if (ret > 0)
  186  				{
  187  					int status;
  188  					waitpid(ret, &status, 0); // keep calm and kill zombies
  189  				}
  190  			}
  191  
  192  			return 0;
  193  #endif
  194  		}
  195  
  196  		int runShutdownCommand()
  197  		{
  198  #ifdef WIN32 // windows
  199  			return system("shutdown -s -t 0");
  200  #else // osx / linux
  201  		return system("shutdown -P -h now");
  202  #endif
  203  		}
  204  
  205  		int runRestartCommand()
  206  		{
  207  #ifdef WIN32 // windows
  208  			return system("shutdown -r -t 0");
  209  #else // osx / linux
  210  			return system("shutdown -r now");
  211  #endif
  212  		}
  213  
  214  		static QuitMode quitMode = QuitMode::QUIT;
  215  
  216  		int quitES(QuitMode mode)
  217  		{
  218  			quitMode = mode;
  219  
  220  			switch (quitMode)
  221  			{
  222  			case QuitMode::REBOOT:
  223  			case QuitMode::FAST_REBOOT:
  224  				Scripting::fireEvent("quit", "reboot");
  225  				Scripting::fireEvent("reboot");
  226  				break;
  227  
  228  			case QuitMode::SHUTDOWN:
  229  			case QuitMode::FAST_SHUTDOWN:
  230  				Scripting::fireEvent("quit", "shutdown");
  231  				Scripting::fireEvent("shutdown");
  232  				break;
  233  			}
  234  
  235  			SDL_Event* quit = new SDL_Event();
  236  			quit->type = SDL_QUIT;
  237  			SDL_PushEvent(quit);
  238  			return 0;
  239  		}
  240  
  241  		void touch(const std::string& filename)
  242  		{
  243  #ifndef WIN32
  244  			int fd = open(filename.c_str(), O_CREAT | O_WRONLY, 0644);
  245  			if (fd >= 0)
  246  				close(fd);
  247  
  248  			// system(("touch " + filename).c_str());
  249  #endif
  250  		}
  251  
  252  		void processQuitMode()
  253  		{
  254  
  255  			switch (quitMode)
  256  			{
  257  			case QuitMode::QUIT:
  258  				Scripting::fireEvent("quit");
  259  				break;
  260  
  261  			case QuitMode::RESTART:
  262  				LOG(LogInfo) << "Restarting EmulationStation";
  263  				touch("/tmp/restart.please");
  264  				break;
  265  			case QuitMode::REBOOT:
  266  			case QuitMode::FAST_REBOOT:
  267  				LOG(LogInfo) << "Rebooting system";
  268  				touch("/tmp/reboot.please");
  269  				runRestartCommand();
  270  				break;
  271  			case QuitMode::SHUTDOWN:
  272  			case QuitMode::FAST_SHUTDOWN:
  273  				LOG(LogInfo) << "Shutting system down";
  274  				touch("/tmp/shutdown.please");
  275  				runShutdownCommand();
  276  				break;
  277  			}
  278  		}
  279  
  280  		bool isFastShutdown()
  281  		{
  282  			return quitMode == QuitMode::FAST_REBOOT || quitMode == QuitMode::FAST_SHUTDOWN;
  283  		}
  284  
  285  #if !WIN32
  286  		// A link of the device's own: up, with a carrier, not loopback and
  287  		// not point-to-point. A tun such as tailscale0 keeps its fixed
  288  		// address whether or not any network carries it, so "the device has
  289  		// an address" is asked of the links alone (fork #279). Upstream's
  290  		// bccd71570 dropped the older list of interface names that did this,
  291  		// and the fork's offline checks had relied on it.
  292  		static bool isLinkInterface(unsigned int flags)
  293  		{
  294  			return (flags & IFF_LOOPBACK) == 0 && (flags & IFF_POINTOPOINT) == 0
  295  				&& (flags & IFF_UP) != 0 && (flags & IFF_RUNNING) != 0;
  296  		}
  297  #endif
  298  
  299  		std::vector<std::string> queryIPAddresses()
  300  		{
  301  			std::vector<std::string> result;
  302  
  303  #ifdef DEVTEST
  304  			result.push_back("127.0.0.1");
  305  			return result;
  306  #endif
  307  
  308  #if WIN32
  309  			// Init WinSock
  310  			WSADATA wsa_Data;
  311  			int wsa_ReturnCode = WSAStartup(0x101, &wsa_Data);
  312  			if (wsa_ReturnCode != 0)
  313  				return result;
  314  
  315  			// Get the local hostname
  316  			char szHostName[255];
  317  			if (gethostname(szHostName, 255) == 0)
  318  			{
  319  				struct hostent* host_entry = gethostbyname(szHostName);
  320  				if (host_entry != nullptr)
  321  					result.push_back(inet_ntoa(*(struct in_addr*)*host_entry->h_addr_list));
  322  			}
  323  			WSACleanup();
  324  #else
  325  			struct ifaddrs* ifAddrStruct = NULL;
  326  			struct ifaddrs* ifa = NULL;
  327  			void* tmpAddrPtr = NULL;
  328  
  329  			getifaddrs(&ifAddrStruct);
  330  
  331  			for (ifa = ifAddrStruct; ifa != NULL; ifa = ifa->ifa_next)
  332  			{
  333  				if (!ifa->ifa_addr)
  334  					continue;
  335  
  336  				// check it is IP4 is a valid IP4 Address
  337  				if (ifa->ifa_addr->sa_family == AF_INET)
  338  				{
  339  					tmpAddrPtr = &((struct sockaddr_in*)ifa->ifa_addr)->sin_addr;
  340  					char addressBuffer[INET_ADDRSTRLEN];
  341  					inet_ntop(AF_INET, tmpAddrPtr, addressBuffer, INET_ADDRSTRLEN);
  342  
  343  					if (isLinkInterface(ifa->ifa_flags))
  344  						result.push_back(std::string(addressBuffer));
  345  				}
  346  			}
  347  
  348  			// Seeking for ipv6 if no IPV4
  349  			if (result.empty())
  350  			{
  351  				for (ifa = ifAddrStruct; ifa != NULL; ifa = ifa->ifa_next)
  352  				{
  353  					if (!ifa->ifa_addr)
  354  						continue;
  355  
  356  					// check it is IP6 is a valid IP6 Address
  357  					if (ifa->ifa_addr->sa_family == AF_INET6)
  358  					{
  359  						tmpAddrPtr = &((struct sockaddr_in6*)ifa->ifa_addr)->sin6_addr;
  360  						char addressBuffer[INET6_ADDRSTRLEN];
  361  						inet_ntop(AF_INET6, tmpAddrPtr, addressBuffer, INET6_ADDRSTRLEN);
  362  
  363  						// Skip IPv6 link-local address
  364  						if (strncmp(addressBuffer, "fe80:", 5) == 0)
  365  							continue;
  366  
  367  						if (isLinkInterface(ifa->ifa_flags))
  368  							result.push_back(std::string(addressBuffer));
  369  					}
  370  				}
  371  			}
  372  
  373  			if (ifAddrStruct != NULL)
  374  				freeifaddrs(ifAddrStruct);
  375  #endif
  376  
  377  			return result;
  378  		}
  379  
  380  		std::vector<InterfaceAddress> queryInterfaceAddresses()
  381  		{
  382  			std::vector<InterfaceAddress> result;
  383  #if !WIN32 && !defined(DEVTEST)
  384  			struct ifaddrs* ifAddrStruct = NULL;
  385  			getifaddrs(&ifAddrStruct);
  386  			for (struct ifaddrs* ifa = ifAddrStruct; ifa != NULL; ifa = ifa->ifa_next)
  387  			{
  388  				if (!ifa->ifa_addr || ifa->ifa_addr->sa_family != AF_INET || (ifa->ifa_flags & IFF_LOOPBACK) != 0)
  389  					continue;
  390  				char addressBuffer[INET_ADDRSTRLEN];
  391  				inet_ntop(AF_INET, &((struct sockaddr_in*)ifa->ifa_addr)->sin_addr, addressBuffer, INET_ADDRSTRLEN);
  392  				result.push_back(InterfaceAddress{ std::string(addressBuffer), std::string(ifa->ifa_name), isLinkInterface(ifa->ifa_flags) });
  393  			}
  394  			if (ifAddrStruct != NULL)
  395  				freeifaddrs(ifAddrStruct);
  396  #endif
  397  			return result;
  398  		}
  399  
  400  		std::string queryIPAddress()
  401  		{
  402  			std::vector<std::string> ips = queryIPAddresses();
  403  			return ips.empty() ? "" : ips.front();
  404  		}
  405  
  406  		BatteryInformation queryBatteryInformation()
  407  		{
  408  			BatteryInformation ret;
  409  			ret.hasBattery = false;
  410  			ret.isCharging = false;
  411  			ret.level = 0;
  412  
  413  #ifdef DEVTEST
  414  			ret.hasBattery = true;
  415  			ret.isCharging = true;
  416  			ret.level = 33;
  417  
  418  			time_t     clockNow = time(0);
  419  			struct tm  clockTstruct = *localtime(&clockNow);
  420  			ret.level = clockTstruct.tm_min;
  421  
  422  			return ret;
  423  #endif
  424  
  425  #ifdef WIN32
  426  			SYSTEM_POWER_STATUS systemPowerStatus;
  427  			if (GetSystemPowerStatus(&systemPowerStatus))
  428  			{
  429  				if ((systemPowerStatus.BatteryFlag & 128) == 128)
  430  					ret.hasBattery = false;
  431  				else
  432  				{
  433  					ret.hasBattery = true;
  434  					ret.isCharging = (systemPowerStatus.BatteryFlag & 8) == 8;
  435  					ret.level = systemPowerStatus.BatteryLifePercent;
  436  				}
  437  			}
  438  			else
  439  				ret.hasBattery = false;
  440  
  441  			return ret;
  442  
  443  #endif
  444  
  445  			static std::string batteryStatusPath;
  446  			static std::string batteryCapacityPath;
  447  			static std::string batteryCurrChargePath;
  448  			static std::string batteryMaxChargePath;
  449  			static std::string batteryCurrentPath;
  450  
  451  			// Find battery path - only at the first call
  452  			if (batteryStatusPath.empty())
  453  			{
  454  				std::string batteryRootPath;
  455  				std::string fuelgaugeRootPath;
  456  				std::string chargerRootPath;
  457  
  458  				auto files = Utils::FileSystem::getDirContent("/sys/class/power_supply");
  459  				for (auto file : files)
  460  				{
  461  					if ((Utils::String::toLower(file).find("/bat") != std::string::npos) && (batteryRootPath.empty()))
  462  						batteryRootPath = file;
  463  
  464  					// Qualcomm devices use "qcom-battery"
  465  					if ((Utils::String::toLower(file).find("/qcom-battery") != std::string::npos) && (batteryRootPath.empty()))
  466  						batteryRootPath = file;
  467  
  468  					if ((Utils::String::toLower(file).find("/qcom-battmgr-bat") != std::string::npos) && (batteryRootPath.empty()))
  469  						batteryRootPath = file;
  470  
  471  					if ((Utils::String::toLower(file).find("fuel") != std::string::npos) && (fuelgaugeRootPath.empty()))
  472  						fuelgaugeRootPath = file;
  473  
  474  					if ((Utils::String::toLower(file).find("charger") != std::string::npos) && (chargerRootPath.empty()))
  475  						chargerRootPath = file;
  476  				}
  477  
  478  				// If there's no battery device, look for discrete charger and fuel gauge
  479  				if (batteryRootPath.empty())
  480  				{
  481  					if (!fuelgaugeRootPath.empty())
  482  					{
  483  						batteryCurrChargePath = fuelgaugeRootPath + "/charge_now";
  484  						batteryMaxChargePath = fuelgaugeRootPath + "/charge_full";
  485  						batteryCapacityPath = ".";
  486  						batteryCurrentPath = ".";
  487  						// If there's a fuel gauge without "charge_now" or "charge_full" property, don't poll it
  488  						if ((!Utils::FileSystem::exists(batteryCurrChargePath)) || (!Utils::FileSystem::exists(batteryMaxChargePath)))
  489  						{
  490  							batteryCurrChargePath = ".";
  491  							batteryMaxChargePath = ".";
  492  						}
  493  					}
  494  					if (!chargerRootPath.empty())
  495  						batteryStatusPath = chargerRootPath + "/status";
  496  					else
  497  						batteryStatusPath = ".";
  498  				}
  499  				else
  500  				{
  501  					batteryStatusPath = batteryRootPath + "/status";
  502  					batteryCapacityPath = batteryRootPath + "/capacity";
  503  					batteryCurrentPath = batteryRootPath + "/current_avg";
  504  				}
  505  			}
  506  
  507  #if defined(BATTERYPLUS)
  508  			if (Utils::FileSystem::exists("/tmp/battery.percent"))
  509  			{
  510  				batteryCapacityPath = "/tmp/battery.percent";
  511  			}
  512  #endif
  513  
  514  			if ((batteryStatusPath.length() <= 1) && (batteryCurrChargePath.length() <= 1))
  515  			{
  516  				ret.hasBattery = false;
  517  				ret.isCharging = false;
  518  				ret.level = 0;
  519  			}
  520  			else
  521  			{
  522  				ret.hasBattery = true;
  523  				std::string chargerStatus;
  524  				chargerStatus = Utils::String::replace(Utils::FileSystem::readAllText(batteryStatusPath), "\n", "");
  525  				ret.isCharging = ((chargerStatus != "Not charging") && (chargerStatus != "Discharging"));
  526  
  527  				if (batteryCurrentPath.length() > 1 && Utils::FileSystem::exists(batteryCurrentPath))
  528  				{
  529  					int currentVal = Utils::String::toInteger(Utils::FileSystem::readAllText(batteryCurrentPath));
  530  					if (currentVal > 0)
  531  						ret.isCharging = true;
  532  				}
  533  
  534  				// If reading from fuel gauge, we have to calculate remaining charge
  535  				if (batteryCapacityPath.length() <= 1)
  536  				{
  537  					if ((!batteryCurrChargePath.empty()) && (!batteryMaxChargePath.empty()))
  538  					{
  539  						float now = std::stof(Utils::FileSystem::readAllText(batteryCurrChargePath).c_str());
  540  						float full = std::stof(Utils::FileSystem::readAllText(batteryMaxChargePath).c_str());
  541  						ret.level = int(round((now / full) * 100));
  542  					}
  543  				}
  544  				else
  545  				{
  546  					std::ifstream file(batteryCapacityPath);
  547  					if (file.is_open())
  548  					{
  549  						std::string buffer;
  550  						std::getline(file, buffer);
  551  						file.close();
  552  						if (!buffer.empty())
  553  						{
  554  							ret.level = Utils::String::toInteger(buffer);
  555  						}
  556  						else
  557  						{
  558  							LOG(LogError) << "Error reading: " << batteryCapacityPath;
  559  						}
  560  					}
  561  					else
  562  					{
  563  						LOG(LogError) << "Error opening: " << batteryCapacityPath;
  564  					}
  565  				}
  566  			}
  567  
  568  			return ret;
  569  		}
  570  
  571  #if WIN32
  572  		static bool _getWindowsVersion(WORD& major, WORD& minor, WORD& build, WORD& revision)
  573  		{
  574  			// Use product version in kernel32.dll to have real Windows version as we don't have a compatibility manifest (GetVersion is limited to 6.2)
  575  			HMODULE kernel32Module = GetModuleHandle("kernel32.dll");
  576  			if (kernel32Module != nullptr)
  577  			{
  578  				wchar_t filePath[MAX_PATH];
  579  				DWORD length = GetModuleFileNameW(kernel32Module, filePath, MAX_PATH);
  580  				if (length > 0)
  581  				{
  582  					DWORD dummy;
  583  					DWORD versionSize = GetFileVersionInfoSizeW(filePath, &dummy);
  584  
  585  					std::vector<char> versionData(versionSize);
  586  					if (GetFileVersionInfoW(filePath, 0, versionSize, versionData.data()))
  587  					{
  588  						VS_FIXEDFILEINFO* fileInfo;
  589  						UINT fileInfoSize;
  590  
  591  						if (VerQueryValueW(versionData.data(), L"\\", reinterpret_cast<void**>(&fileInfo), &fileInfoSize))
  592  						{
  593  						    major = HIWORD(fileInfo->dwProductVersionMS);
  594  							minor = LOWORD(fileInfo->dwProductVersionMS);
  595  							build = HIWORD(fileInfo->dwProductVersionLS);
  596  							revision = LOWORD(fileInfo->dwProductVersionLS);
  597  
  598  							return true;
  599  						}
  600  					}
  601  				}
  602  			}
  603  
  604  			return false;
  605  		}
  606  
  607  		bool isWindows10()
  608  		{
  609  			static const bool result = []()
  610  			{
  611  				WORD major, minor, build, revision;
  612  
  613  				if (_getWindowsVersion(major, minor, build, revision))
  614  					return major > 10 || (major == 10);
  615  
  616  				return false;
  617  			}();
  618  
  619  			return result;
  620  		}
  621  
  622  		bool isWindows11()
  623  		{
  624  			static const bool result = []()
  625  			{
  626  				WORD major, minor, build, revision;
  627  
  628  				if (_getWindowsVersion(major, minor, build, revision))
  629  					return major > 10 || (major == 10 && (minor > 0 || build >= 22000));
  630  
  631  				return false;
  632  			}();
  633  
  634  			return result;
  635  		}
  636  
  637  		// Declared locally (instead of pulled from ShellScalingApi.h / a newer
  638  		// winuser.h) so this builds regardless of which Windows SDK version ES is
  639  		// compiled against; on older SDKs the constant/type simply doesn't exist yet.
  640  #ifndef DPI_AWARENESS_CONTEXT_PER_MONITOR_AWARE_V2
  641  		DECLARE_HANDLE(DPI_AWARENESS_CONTEXT);
  642  #define DPI_AWARENESS_CONTEXT_PER_MONITOR_AWARE_V2 ((DPI_AWARENESS_CONTEXT)-4)
  643  #endif
  644  
  645  		typedef BOOL(WINAPI* SetProcessDpiAwarenessContext_t)(DPI_AWARENESS_CONTEXT);
  646  		typedef HRESULT(WINAPI* SetProcessDpiAwareness_t)(int);
  647  		typedef BOOL(WINAPI* SetProcessDPIAware_t)();
  648  
  649  		// Marks the process Per-Monitor-V2 DPI aware so Windows stops bitmap-
  650  		// stretching our output on displays scaled above 100% (e.g. 4K @ 150%).
  651  		// Without this, ES is treated as DPI-unaware, gets handed a virtualized
  652  		// logical resolution, and users have to manually enable the "Override high
  653  		// DPI scaling" compatibility option for fullscreen/video sizing to be correct.
  654  		// Resolved dynamically (rather than via an app manifest or direct linking) so
  655  		// the same binary degrades gracefully on Windows 8.1/7, where PMv2 and even
  656  		// PROCESS_PER_MONITOR_DPI_AWARE don't exist.
  657  		void setDpiAwareness()
  658  		{
  659  			HMODULE user32 = LoadLibraryA("user32.dll");
  660  			if (user32 != NULL)
  661  			{
  662  				auto setContext = (SetProcessDpiAwarenessContext_t)GetProcAddress(user32, "SetProcessDpiAwarenessContext");
  663  				if (setContext != NULL && setContext(DPI_AWARENESS_CONTEXT_PER_MONITOR_AWARE_V2))
  664  				{
  665  					FreeLibrary(user32);
  666  					return;
  667  				}
  668  			}
  669  
  670  			HMODULE shcore = LoadLibraryA("Shcore.dll");
  671  			if (shcore != NULL)
  672  			{
  673  				auto setAwareness = (SetProcessDpiAwareness_t)GetProcAddress(shcore, "SetProcessDpiAwareness");
  674  				if (setAwareness != NULL && SUCCEEDED(setAwareness(2 /* PROCESS_PER_MONITOR_DPI_AWARE */)))
  675  				{
  676  					FreeLibrary(shcore);
  677  					if (user32 != NULL)
  678  						FreeLibrary(user32);
  679  					return;
  680  				}
  681  
  682  				FreeLibrary(shcore);
  683  			}
  684  
  685  			if (user32 != NULL)
  686  			{
  687  				auto setAware = (SetProcessDPIAware_t)GetProcAddress(user32, "SetProcessDPIAware");
  688  				if (setAware != NULL)
  689  					setAware();
  690  
  691  				FreeLibrary(user32);
  692  			}
  693  		}
  694  #else
  695  		bool isBuildroot()
  696  		{
  697  			static const bool cached = []() 
  698  			{
  699  				std::ifstream f("/etc/os-release");
  700  				if (!f)
  701  					return false;
  702  
  703  				std::string line;
  704  				while (std::getline(f, line))
  705  					if (line == "ID=buildroot")
  706  						return true;
  707  
  708  				return false;
  709  			}();
  710  
  711  			return cached;
  712  		}
  713  #endif
  714  
  715  		std::string getArchString()
  716  		{
  717  #if WIN32
  718  			return "windows";
  719  #else
  720  			std::string arch = Utils::FileSystem::readAllText("/usr/share/batocera/batocera.arch");
  721  			if (!arch.empty())
  722  				return arch;
  723  
  724  #if X86
  725  			return "x86";
  726  #endif
  727  
  728  #if X86_64
  729  			return "x86_64";
  730  #endif
  731  
  732  #if RPIZERO2
  733  			return "rpizero2";
  734  #endif
  735  
  736  #if RPI1 || BCM2835
  737  			return "rpi1";
  738  #endif
  739  
  740  #if RPI2
  741  			return "rpi2";
  742  #endif
  743  
  744  #if RPI3 || BCM2836 || BCM2837
  745  			return "rpi3";
  746  #endif
  747  
  748  #if RPI4 || BCM2711
  749  			return "rpi4";
  750  #endif
  751  
  752  #if ODROIDXU4
  753  			return "odroidxu4";
  754  #endif
  755  
  756  #if RK3128
  757  			return "rk3128";
  758  #endif
  759  
  760  #if RK3288
  761  			return "rk3288";
  762  #endif
  763  
  764  #if RK3326
  765  			return "rk3326";
  766  #endif
  767  
  768  #if RK3328
  769  			return "rk3328";
  770  #endif
  771  
  772  #if RK3399
  773  			return "rk3399";
  774  #endif
  775  
  776  #if RK3566
  777  			return "rk3566";
  778  #endif
  779  
  780  #if RK3568
  781  			return "rk3568";
  782  #endif
  783  
  784  #if RK3576
  785  			return "rk3576";
  786  #endif
  787  
  788  #if RK3588
  789  			return "rk3588";
  790  #endif
  791  
  792  #if H3
  793  			return "h3";
  794  #endif
  795  
  796  #if H5
  797  			return "h5";
  798  #endif
  799  
  800  #if H6
  801  			return "h6";
  802  #endif
  803  
  804  #if H616
  805  			return "h616";
  806  #endif
  807  
  808  #if S812
  809  			return "s812";
  810  #endif
  811  
  812  #if S905
  813  			return "s905";
  814  #endif
  815  
  816  #if S912
  817  			return "s912";
  818  #endif
  819  
  820  #if S905GEN2
  821  			return "s905gen2";
  822  #endif
  823  
  824  #if S905GEN3
  825  			return "s905gen3";
  826  #endif
  827  
  828  #if S922X
  829  			return "s922x";
  830  #endif
  831  
  832  #if SM6115
  833  			return "sm6115";
  834  #endif
  835  
  836  #if SM8250
  837  			return "sm8250";
  838  #endif
  839  
  840  #if SM8550
  841  			return "sm8550";
  842  #endif
  843  
  844  #if SM8650
  845  			return "sm8650";
  846  #endif
  847  
  848  #endif
  849  
  850  			return "";
  851  		}
  852  
  853  		int runSystemCommand(const std::string& cmd_utf8, const std::string& name, Window* window)
  854  		{
  855  			LOG(LogInfo) << "runSystemCommand: " + Utils::String::maskSecrets(cmd_utf8);
  856  
  857  			// Parent fork
  858  			pid_t ret = fork();
  859  			if (ret == 0)
  860  			{
  861  				ret = fork();
  862  				if (ret == 0)
  863  				{
  864  					execl("/usr/bin/sh", "sh", "-c", (cmd_utf8).c_str(), (char *) NULL);
  865  					_exit(1); // execl failed
  866  				}
  867  				int status;
  868  				waitpid(ret, &status, 0); // Wait for fork exit..
  869  				_exit(0);
  870  			}
  871  			else
  872  			{
  873  				if (ret > 0)
  874  				{
  875  					int status;
  876  					waitpid(ret, &status, 0); // keep calm and kill zombies
  877  				}
  878  			}
  879  			return 0;
  880  		}
  881  
  882  		std::string GetEnv(const std::string& var) {
  883  			const char* val = std::getenv(var.c_str());
  884  			if (val == nullptr) {
  885  				return "";
  886  			} else {
  887  				return val;
  888  			}
  889  		}
  890  
  891  		std::string GetShOutput(const std::string& mStr)
  892  		{
  893  			std::string result, file;
  894  			FILE* pipe{popen(mStr.c_str(), "r")};
  895  			char buffer[256];
  896  
  897  			while(fgets(buffer, sizeof(buffer), pipe) != NULL)
  898  			{
  899  				file = buffer;
  900  				result += file.substr(0, file.size() - 1);
  901  			}
  902  
  903  			pclose(pipe);
  904  			return result;
  905  		}
  906  
  907  		std::vector<std::string> GetShOutputLines(const std::string& mStr)
  908  		{
  909  			std::vector<std::string> lines;
  910  
  911  			FILE* pipe = popen(mStr.c_str(), "r");
  912  			if (pipe == nullptr)
  913  				return lines;
  914  
  915  			// Accumulate rather than treating each fgets() as a line: a line
  916  			// longer than the buffer arrives in several reads, and only the
  917  			// last of them carries the newline.
  918  			std::string pending;
  919  			char buffer[512];
  920  			while (fgets(buffer, sizeof(buffer), pipe) != NULL)
  921  			{
  922  				pending += buffer;
  923  				size_t nl;
  924  				while ((nl = pending.find('\n')) != std::string::npos)
  925  				{
  926  					lines.push_back(pending.substr(0, nl));
  927  					pending.erase(0, nl + 1);
  928  				}
  929  			}
  930  			if (!pending.empty())
  931  				lines.push_back(pending);
  932  
  933  			pclose(pipe);
  934  			return lines;
  935  		}
  936  
  937  		unsigned long long getTotalSystemMemory() 
  938  		{
  939  #ifdef WIN32
  940  			MEMORYSTATUSEX status;
  941  			status.dwLength = sizeof(status);
  942  			if (GlobalMemoryStatusEx(&status))
  943  				return status.ullTotalPhys;
  944  			
  945  			return 0;
  946  #else
  947  			long pages = sysconf(_SC_PHYS_PAGES);
  948  			long page_size = sysconf(_SC_PAGE_SIZE);
  949  			if (pages == -1 || page_size == -1)
  950  				return 0;
  951  			
  952  			return (unsigned long long)pages * (unsigned long long)page_size;
  953  #endif
  954  		}
  955  	}
  956  }
```

## src/utils/Platform.h (whole, fork-modified, at the pin)

```text
    1  #pragma once
    2  #ifndef ES_CORE_PLATFORM_H
    3  #define ES_CORE_PLATFORM_H
    4  
    5  #include <string>
    6  #include <vector>
    7  
    8  #ifdef WIN32
    9  #include <Windows.h>
   10  #include <intrin.h>
   11  
   12  #define sleep Sleep
   13  #endif
   14  
   15  class Window;
   16  
   17  namespace Utils
   18  {
   19  	namespace Platform
   20  	{
   21  		enum QuitMode
   22  		{
   23  			QUIT = 0,
   24  			RESTART = 1,
   25  			SHUTDOWN = 2,
   26  			REBOOT = 3,
   27  			FAST_SHUTDOWN = 4,
   28  			FAST_REBOOT = 5
   29  		};
   30  
   31  		class ProcessStartInfo
   32  		{
   33  		public:
   34  			ProcessStartInfo();
   35  			ProcessStartInfo(const std::string& cmd);
   36  
   37  			int run() const;
   38  
   39  			std::string command;			
   40  			bool waitForExit;
   41  			bool showWindow;
   42  			Window* window;
   43  #ifndef WIN32
   44  			std::string stderrFilename;
   45  			std::string stdoutFilename;
   46  #endif
   47  		};
   48  
   49  		int quitES(QuitMode mode = QuitMode::QUIT);
   50  		bool isFastShutdown();
   51  		void processQuitMode();
   52  
   53  		struct BatteryInformation
   54  		{
   55  			BatteryInformation()
   56  			{
   57  				hasBattery = false;
   58  				level = 0;
   59  				isCharging = false;
   60  			}
   61  
   62  			bool hasBattery;
   63  			int  level;
   64  			bool isCharging;
   65  		};
   66  
   67  		BatteryInformation queryBatteryInformation();
   68  
   69  		// One address on one interface, and whether that interface is a link
   70  		// of the device's own -- up, with a carrier, not loopback, not
   71  		// point-to-point -- as against a tunnel such as tailscale0, which
   72  		// keeps its fixed address whether or not any network carries it
   73  		// (fork #279). queryIPAddresses() is the physical ones, IPv4 first,
   74  		// and is what every "is the device connected" question reads.
   75  		struct InterfaceAddress { std::string address; std::string interface; bool physical; };
   76  		std::vector<InterfaceAddress> queryInterfaceAddresses();
   77  		std::vector<std::string> queryIPAddresses();
   78  		std::string queryIPAddress();
   79  		std::string getArchString();
   80  		unsigned long long getTotalSystemMemory();
   81  
   82  #if WIN32
   83  		bool isWindows10();
   84  		bool isWindows11();
   85  		void setDpiAwareness();
   86  #else
   87  		bool isBuildroot();
   88  #endif
   89  		int runSystemCommand(const std::string& cmd_utf8, const std::string& name, Window* window); // run a utf-8 encoded in the shell (requires wstring conversion on Windows)
   90  		std::string GetEnv(const std::string& var);
   91  		std::string GetShOutput(const std::string& mStr);
   92  		// GetShOutput concatenates its input into a single string, dropping the
   93  		// last character of every chunk it reads -- which is the newline. That is
   94  		// what its single-line callers want, and useless for a command that emits
   95  		// one record per line. This returns the lines instead.
   96  		std::vector<std::string> GetShOutputLines(const std::string& mStr);
   97  	}
   98  }
   99  
  100  #endif // ES_CORE_PLATFORM_H
```

## src/utils/StringUtil.cpp (whole, fork-modified, at the pin)

```text
    1  #include "utils/StringUtil.h"
    2  
    3  #include <algorithm>
    4  #include <stdarg.h>
    5  #include <cstring>
    6  
    7  #if defined(_WIN32)
    8  #include <Windows.h>
    9  #include <ctype.h>
   10  #else
   11  #include <unistd.h>
   12  #endif
   13  
   14  #include "han.h"
   15  
   16  namespace Utils
   17  {
   18  	namespace String
   19  	{
   20  		static wchar_t unicode_lowers[] =
   21  		{
   22  			(wchar_t)0x0061, (wchar_t)0x0062, (wchar_t)0x0063, (wchar_t)0x0064, (wchar_t)0x0065, (wchar_t)0x0066, (wchar_t)0x0067, (wchar_t)0x0068, (wchar_t)0x0069,
   23  			(wchar_t)0x006A, (wchar_t)0x006B, (wchar_t)0x006C, (wchar_t)0x006D, (wchar_t)0x006E, (wchar_t)0x006F, (wchar_t)0x0070, (wchar_t)0x0071, (wchar_t)0x0072,
   24  			(wchar_t)0x0073, (wchar_t)0x0074, (wchar_t)0x0075, (wchar_t)0x0076, (wchar_t)0x0077, (wchar_t)0x0078, (wchar_t)0x0079, (wchar_t)0x007A, (wchar_t)0x00E0,
   25  			(wchar_t)0x00E1, (wchar_t)0x00E2, (wchar_t)0x00E3, (wchar_t)0x00E4, (wchar_t)0x00E5, (wchar_t)0x00E6, (wchar_t)0x00E7, (wchar_t)0x00E8, (wchar_t)0x00E9,
   26  			(wchar_t)0x00EA, (wchar_t)0x00EB, (wchar_t)0x00EC, (wchar_t)0x00ED, (wchar_t)0x00EE, (wchar_t)0x00EF, (wchar_t)0x00F0, (wchar_t)0x00F1, (wchar_t)0x00F2,
   27  			(wchar_t)0x00F3, (wchar_t)0x00F4, (wchar_t)0x00F5, (wchar_t)0x00F6, (wchar_t)0x00F8, (wchar_t)0x00F9, (wchar_t)0x00FA, (wchar_t)0x00FB, (wchar_t)0x00FC,
   28  			(wchar_t)0x00FD, (wchar_t)0x00FE, (wchar_t)0x00FF, (wchar_t)0x0101, (wchar_t)0x0103, (wchar_t)0x0105, (wchar_t)0x0107, (wchar_t)0x0109, (wchar_t)0x010B,
   29  			(wchar_t)0x010D, (wchar_t)0x010F, (wchar_t)0x0111, (wchar_t)0x0113, (wchar_t)0x0115, (wchar_t)0x0117, (wchar_t)0x0119, (wchar_t)0x011B, (wchar_t)0x011D,
   30  			(wchar_t)0x011F, (wchar_t)0x0121, (wchar_t)0x0123, (wchar_t)0x0125, (wchar_t)0x0127, (wchar_t)0x0129, (wchar_t)0x012B, (wchar_t)0x012D, (wchar_t)0x012F,
   31  			(wchar_t)0x0131, (wchar_t)0x0133, (wchar_t)0x0135, (wchar_t)0x0137, (wchar_t)0x013A, (wchar_t)0x013C, (wchar_t)0x013E, (wchar_t)0x0140, (wchar_t)0x0142,
   32  			(wchar_t)0x0144, (wchar_t)0x0146, (wchar_t)0x0148, (wchar_t)0x014B, (wchar_t)0x014D, (wchar_t)0x014F, (wchar_t)0x0151, (wchar_t)0x0153, (wchar_t)0x0155,
   33  			(wchar_t)0x0157, (wchar_t)0x0159, (wchar_t)0x015B, (wchar_t)0x015D, (wchar_t)0x015F, (wchar_t)0x0161, (wchar_t)0x0163, (wchar_t)0x0165, (wchar_t)0x0167,
   34  			(wchar_t)0x0169, (wchar_t)0x016B, (wchar_t)0x016D, (wchar_t)0x016F, (wchar_t)0x0171, (wchar_t)0x0173, (wchar_t)0x0175, (wchar_t)0x0177, (wchar_t)0x017A,
   35  			(wchar_t)0x017C, (wchar_t)0x017E, (wchar_t)0x0183, (wchar_t)0x0185, (wchar_t)0x0188, (wchar_t)0x018C, (wchar_t)0x0192, (wchar_t)0x0199, (wchar_t)0x01A1,
   36  			(wchar_t)0x01A3, (wchar_t)0x01A5, (wchar_t)0x01A8, (wchar_t)0x01AD, (wchar_t)0x01B0, (wchar_t)0x01B4, (wchar_t)0x01B6, (wchar_t)0x01B9, (wchar_t)0x01BD,
   37  			(wchar_t)0x01C6, (wchar_t)0x01C9, (wchar_t)0x01CC, (wchar_t)0x01CE, (wchar_t)0x01D0, (wchar_t)0x01D2, (wchar_t)0x01D4, (wchar_t)0x01D6, (wchar_t)0x01D8,
   38  			(wchar_t)0x01DA, (wchar_t)0x01DC, (wchar_t)0x01DF, (wchar_t)0x01E1, (wchar_t)0x01E3, (wchar_t)0x01E5, (wchar_t)0x01E7, (wchar_t)0x01E9, (wchar_t)0x01EB,
   39  			(wchar_t)0x01ED, (wchar_t)0x01EF, (wchar_t)0x01F3, (wchar_t)0x01F5, (wchar_t)0x01FB, (wchar_t)0x01FD, (wchar_t)0x01FF, (wchar_t)0x0201, (wchar_t)0x0203,
   40  			(wchar_t)0x0205, (wchar_t)0x0207, (wchar_t)0x0209, (wchar_t)0x020B, (wchar_t)0x020D, (wchar_t)0x020F, (wchar_t)0x0211, (wchar_t)0x0213, (wchar_t)0x0215,
   41  			(wchar_t)0x0217, (wchar_t)0x0253, (wchar_t)0x0254, (wchar_t)0x0257, (wchar_t)0x0258, (wchar_t)0x0259, (wchar_t)0x025B, (wchar_t)0x0260, (wchar_t)0x0263,
   42  			(wchar_t)0x0268, (wchar_t)0x0269, (wchar_t)0x026F, (wchar_t)0x0272, (wchar_t)0x0275, (wchar_t)0x0283, (wchar_t)0x0288, (wchar_t)0x028A, (wchar_t)0x028B,
   43  			(wchar_t)0x0292, (wchar_t)0x03AC, (wchar_t)0x03AD, (wchar_t)0x03AE, (wchar_t)0x03AF, (wchar_t)0x03B1, (wchar_t)0x03B2, (wchar_t)0x03B3, (wchar_t)0x03B4,
   44  			(wchar_t)0x03B5, (wchar_t)0x03B6, (wchar_t)0x03B7, (wchar_t)0x03B8, (wchar_t)0x03B9, (wchar_t)0x03BA, (wchar_t)0x03BB, (wchar_t)0x03BC, (wchar_t)0x03BD,
   45  			(wchar_t)0x03BE, (wchar_t)0x03BF, (wchar_t)0x03C0, (wchar_t)0x03C1, (wchar_t)0x03C3, (wchar_t)0x03C4, (wchar_t)0x03C5, (wchar_t)0x03C6, (wchar_t)0x03C7,
   46  			(wchar_t)0x03C8, (wchar_t)0x03C9, (wchar_t)0x03CA, (wchar_t)0x03CB, (wchar_t)0x03CC, (wchar_t)0x03CD, (wchar_t)0x03CE, (wchar_t)0x03E3, (wchar_t)0x03E5,
   47  			(wchar_t)0x03E7, (wchar_t)0x03E9, (wchar_t)0x03EB, (wchar_t)0x03ED, (wchar_t)0x03EF, (wchar_t)0x0430, (wchar_t)0x0431, (wchar_t)0x0432, (wchar_t)0x0433,
   48  			(wchar_t)0x0434, (wchar_t)0x0435, (wchar_t)0x0436, (wchar_t)0x0437, (wchar_t)0x0438, (wchar_t)0x0439, (wchar_t)0x043A, (wchar_t)0x043B, (wchar_t)0x043C,
   49  			(wchar_t)0x043D, (wchar_t)0x043E, (wchar_t)0x043F, (wchar_t)0x0440, (wchar_t)0x0441, (wchar_t)0x0442, (wchar_t)0x0443, (wchar_t)0x0444, (wchar_t)0x0445,
   50  			(wchar_t)0x0446, (wchar_t)0x0447, (wchar_t)0x0448, (wchar_t)0x0449, (wchar_t)0x044A, (wchar_t)0x044B, (wchar_t)0x044C, (wchar_t)0x044D, (wchar_t)0x044E,
   51  			(wchar_t)0x044F, (wchar_t)0x0451, (wchar_t)0x0452, (wchar_t)0x0453, (wchar_t)0x0454, (wchar_t)0x0455, (wchar_t)0x0456, (wchar_t)0x0457, (wchar_t)0x0458,
   52  			(wchar_t)0x0459, (wchar_t)0x045A, (wchar_t)0x045B, (wchar_t)0x045C, (wchar_t)0x045E, (wchar_t)0x045F, (wchar_t)0x0461, (wchar_t)0x0463, (wchar_t)0x0465,
   53  			(wchar_t)0x0467, (wchar_t)0x0469, (wchar_t)0x046B, (wchar_t)0x046D, (wchar_t)0x046F, (wchar_t)0x0471, (wchar_t)0x0473, (wchar_t)0x0475, (wchar_t)0x0477,
   54  			(wchar_t)0x0479, (wchar_t)0x047B, (wchar_t)0x047D, (wchar_t)0x047F, (wchar_t)0x0481, (wchar_t)0x0491, (wchar_t)0x0493, (wchar_t)0x0495, (wchar_t)0x0497,
   55  			(wchar_t)0x0499, (wchar_t)0x049B, (wchar_t)0x049D, (wchar_t)0x049F, (wchar_t)0x04A1, (wchar_t)0x04A3, (wchar_t)0x04A5, (wchar_t)0x04A7, (wchar_t)0x04A9,
   56  			(wchar_t)0x04AB, (wchar_t)0x04AD, (wchar_t)0x04AF, (wchar_t)0x04B1, (wchar_t)0x04B3, (wchar_t)0x04B5, (wchar_t)0x04B7, (wchar_t)0x04B9, (wchar_t)0x04BB,
   57  			(wchar_t)0x04BD, (wchar_t)0x04BF, (wchar_t)0x04C2, (wchar_t)0x04C4, (wchar_t)0x04C8, (wchar_t)0x04CC, (wchar_t)0x04D1, (wchar_t)0x04D3, (wchar_t)0x04D5,
   58  			(wchar_t)0x04D7, (wchar_t)0x04D9, (wchar_t)0x04DB, (wchar_t)0x04DD, (wchar_t)0x04DF, (wchar_t)0x04E1, (wchar_t)0x04E3, (wchar_t)0x04E5, (wchar_t)0x04E7,
   59  			(wchar_t)0x04E9, (wchar_t)0x04EB, (wchar_t)0x04EF, (wchar_t)0x04F1, (wchar_t)0x04F3, (wchar_t)0x04F5, (wchar_t)0x04F9, (wchar_t)0x0561, (wchar_t)0x0562,
   60  			(wchar_t)0x0563, (wchar_t)0x0564, (wchar_t)0x0565, (wchar_t)0x0566, (wchar_t)0x0567, (wchar_t)0x0568, (wchar_t)0x0569, (wchar_t)0x056A, (wchar_t)0x056B,
   61  			(wchar_t)0x056C, (wchar_t)0x056D, (wchar_t)0x056E, (wchar_t)0x056F, (wchar_t)0x0570, (wchar_t)0x0571, (wchar_t)0x0572, (wchar_t)0x0573, (wchar_t)0x0574,
   62  			(wchar_t)0x0575, (wchar_t)0x0576, (wchar_t)0x0577, (wchar_t)0x0578, (wchar_t)0x0579, (wchar_t)0x057A, (wchar_t)0x057B, (wchar_t)0x057C, (wchar_t)0x057D,
   63  			(wchar_t)0x057E, (wchar_t)0x057F, (wchar_t)0x0580, (wchar_t)0x0581, (wchar_t)0x0582, (wchar_t)0x0583, (wchar_t)0x0584, (wchar_t)0x0585, (wchar_t)0x0586,
   64  			(wchar_t)0x10D0, (wchar_t)0x10D1, (wchar_t)0x10D2, (wchar_t)0x10D3, (wchar_t)0x10D4, (wchar_t)0x10D5, (wchar_t)0x10D6, (wchar_t)0x10D7, (wchar_t)0x10D8,
   65  			(wchar_t)0x10D9, (wchar_t)0x10DA, (wchar_t)0x10DB, (wchar_t)0x10DC, (wchar_t)0x10DD, (wchar_t)0x10DE, (wchar_t)0x10DF, (wchar_t)0x10E0, (wchar_t)0x10E1,
   66  			(wchar_t)0x10E2, (wchar_t)0x10E3, (wchar_t)0x10E4, (wchar_t)0x10E5, (wchar_t)0x10E6, (wchar_t)0x10E7, (wchar_t)0x10E8, (wchar_t)0x10E9, (wchar_t)0x10EA,
   67  			(wchar_t)0x10EB, (wchar_t)0x10EC, (wchar_t)0x10ED, (wchar_t)0x10EE, (wchar_t)0x10EF, (wchar_t)0x10F0, (wchar_t)0x10F1, (wchar_t)0x10F2, (wchar_t)0x10F3,
   68  			(wchar_t)0x10F4, (wchar_t)0x10F5, (wchar_t)0x1E01, (wchar_t)0x1E03, (wchar_t)0x1E05, (wchar_t)0x1E07, (wchar_t)0x1E09, (wchar_t)0x1E0B, (wchar_t)0x1E0D,
   69  			(wchar_t)0x1E0F, (wchar_t)0x1E11, (wchar_t)0x1E13, (wchar_t)0x1E15, (wchar_t)0x1E17, (wchar_t)0x1E19, (wchar_t)0x1E1B, (wchar_t)0x1E1D, (wchar_t)0x1E1F,
   70  			(wchar_t)0x1E21, (wchar_t)0x1E23, (wchar_t)0x1E25, (wchar_t)0x1E27, (wchar_t)0x1E29, (wchar_t)0x1E2B, (wchar_t)0x1E2D, (wchar_t)0x1E2F, (wchar_t)0x1E31,
   71  			(wchar_t)0x1E33, (wchar_t)0x1E35, (wchar_t)0x1E37, (wchar_t)0x1E39, (wchar_t)0x1E3B, (wchar_t)0x1E3D, (wchar_t)0x1E3F, (wchar_t)0x1E41, (wchar_t)0x1E43,
   72  			(wchar_t)0x1E45, (wchar_t)0x1E47, (wchar_t)0x1E49, (wchar_t)0x1E4B, (wchar_t)0x1E4D, (wchar_t)0x1E4F, (wchar_t)0x1E51, (wchar_t)0x1E53, (wchar_t)0x1E55,
   73  			(wchar_t)0x1E57, (wchar_t)0x1E59, (wchar_t)0x1E5B, (wchar_t)0x1E5D, (wchar_t)0x1E5F, (wchar_t)0x1E61, (wchar_t)0x1E63, (wchar_t)0x1E65, (wchar_t)0x1E67,
   74  			(wchar_t)0x1E69, (wchar_t)0x1E6B, (wchar_t)0x1E6D, (wchar_t)0x1E6F, (wchar_t)0x1E71, (wchar_t)0x1E73, (wchar_t)0x1E75, (wchar_t)0x1E77, (wchar_t)0x1E79,
   75  			(wchar_t)0x1E7B, (wchar_t)0x1E7D, (wchar_t)0x1E7F, (wchar_t)0x1E81, (wchar_t)0x1E83, (wchar_t)0x1E85, (wchar_t)0x1E87, (wchar_t)0x1E89, (wchar_t)0x1E8B,
   76  			(wchar_t)0x1E8D, (wchar_t)0x1E8F, (wchar_t)0x1E91, (wchar_t)0x1E93, (wchar_t)0x1E95, (wchar_t)0x1EA1, (wchar_t)0x1EA3, (wchar_t)0x1EA5, (wchar_t)0x1EA7,
   77  			(wchar_t)0x1EA9, (wchar_t)0x1EAB, (wchar_t)0x1EAD, (wchar_t)0x1EAF, (wchar_t)0x1EB1, (wchar_t)0x1EB3, (wchar_t)0x1EB5, (wchar_t)0x1EB7, (wchar_t)0x1EB9,
   78  			(wchar_t)0x1EBB, (wchar_t)0x1EBD, (wchar_t)0x1EBF, (wchar_t)0x1EC1, (wchar_t)0x1EC3, (wchar_t)0x1EC5, (wchar_t)0x1EC7, (wchar_t)0x1EC9, (wchar_t)0x1ECB,
   79  			(wchar_t)0x1ECD, (wchar_t)0x1ECF, (wchar_t)0x1ED1, (wchar_t)0x1ED3, (wchar_t)0x1ED5, (wchar_t)0x1ED7, (wchar_t)0x1ED9, (wchar_t)0x1EDB, (wchar_t)0x1EDD,
   80  			(wchar_t)0x1EDF, (wchar_t)0x1EE1, (wchar_t)0x1EE3, (wchar_t)0x1EE5, (wchar_t)0x1EE7, (wchar_t)0x1EE9, (wchar_t)0x1EEB, (wchar_t)0x1EED, (wchar_t)0x1EEF,
   81  			(wchar_t)0x1EF1, (wchar_t)0x1EF3, (wchar_t)0x1EF5, (wchar_t)0x1EF7, (wchar_t)0x1EF9, (wchar_t)0x1F00, (wchar_t)0x1F01, (wchar_t)0x1F02, (wchar_t)0x1F03,
   82  			(wchar_t)0x1F04, (wchar_t)0x1F05, (wchar_t)0x1F06, (wchar_t)0x1F07, (wchar_t)0x1F10, (wchar_t)0x1F11, (wchar_t)0x1F12, (wchar_t)0x1F13, (wchar_t)0x1F14,
   83  			(wchar_t)0x1F15, (wchar_t)0x1F20, (wchar_t)0x1F21, (wchar_t)0x1F22, (wchar_t)0x1F23, (wchar_t)0x1F24, (wchar_t)0x1F25, (wchar_t)0x1F26, (wchar_t)0x1F27,
   84  			(wchar_t)0x1F30, (wchar_t)0x1F31, (wchar_t)0x1F32, (wchar_t)0x1F33, (wchar_t)0x1F34, (wchar_t)0x1F35, (wchar_t)0x1F36, (wchar_t)0x1F37, (wchar_t)0x1F40,
   85  			(wchar_t)0x1F41, (wchar_t)0x1F42, (wchar_t)0x1F43, (wchar_t)0x1F44, (wchar_t)0x1F45, (wchar_t)0x1F51, (wchar_t)0x1F53, (wchar_t)0x1F55, (wchar_t)0x1F57,
   86  			(wchar_t)0x1F60, (wchar_t)0x1F61, (wchar_t)0x1F62, (wchar_t)0x1F63, (wchar_t)0x1F64, (wchar_t)0x1F65, (wchar_t)0x1F66, (wchar_t)0x1F67, (wchar_t)0x1F80,
   87  			(wchar_t)0x1F81, (wchar_t)0x1F82, (wchar_t)0x1F83, (wchar_t)0x1F84, (wchar_t)0x1F85, (wchar_t)0x1F86, (wchar_t)0x1F87, (wchar_t)0x1F90, (wchar_t)0x1F91,
   88  			(wchar_t)0x1F92, (wchar_t)0x1F93, (wchar_t)0x1F94, (wchar_t)0x1F95, (wchar_t)0x1F96, (wchar_t)0x1F97, (wchar_t)0x1FA0, (wchar_t)0x1FA1, (wchar_t)0x1FA2,
   89  			(wchar_t)0x1FA3, (wchar_t)0x1FA4, (wchar_t)0x1FA5, (wchar_t)0x1FA6, (wchar_t)0x1FA7, (wchar_t)0x1FB0, (wchar_t)0x1FB1, (wchar_t)0x1FD0, (wchar_t)0x1FD1,
   90  			(wchar_t)0x1FE0, (wchar_t)0x1FE1, (wchar_t)0x24D0, (wchar_t)0x24D1, (wchar_t)0x24D2, (wchar_t)0x24D3, (wchar_t)0x24D4, (wchar_t)0x24D5, (wchar_t)0x24D6,
   91  			(wchar_t)0x24D7, (wchar_t)0x24D8, (wchar_t)0x24D9, (wchar_t)0x24DA, (wchar_t)0x24DB, (wchar_t)0x24DC, (wchar_t)0x24DD, (wchar_t)0x24DE, (wchar_t)0x24DF,
   92  			(wchar_t)0x24E0, (wchar_t)0x24E1, (wchar_t)0x24E2, (wchar_t)0x24E3, (wchar_t)0x24E4, (wchar_t)0x24E5, (wchar_t)0x24E6, (wchar_t)0x24E7, (wchar_t)0x24E8,
   93  			(wchar_t)0x24E9, (wchar_t)0xFF41, (wchar_t)0xFF42, (wchar_t)0xFF43, (wchar_t)0xFF44, (wchar_t)0xFF45, (wchar_t)0xFF46, (wchar_t)0xFF47, (wchar_t)0xFF48,
   94  			(wchar_t)0xFF49, (wchar_t)0xFF4A, (wchar_t)0xFF4B, (wchar_t)0xFF4C, (wchar_t)0xFF4D, (wchar_t)0xFF4E, (wchar_t)0xFF4F, (wchar_t)0xFF50, (wchar_t)0xFF51,
   95  			(wchar_t)0xFF52, (wchar_t)0xFF53, (wchar_t)0xFF54, (wchar_t)0xFF55, (wchar_t)0xFF56, (wchar_t)0xFF57, (wchar_t)0xFF58, (wchar_t)0xFF59, (wchar_t)0xFF5A };
   96  
   97  		static const wchar_t unicode_uppers[] =
   98  		{
   99  			(wchar_t)0x0041, (wchar_t)0x0042, (wchar_t)0x0043, (wchar_t)0x0044, (wchar_t)0x0045, (wchar_t)0x0046, (wchar_t)0x0047, (wchar_t)0x0048, (wchar_t)0x0049,
  100  			(wchar_t)0x004A, (wchar_t)0x004B, (wchar_t)0x004C, (wchar_t)0x004D, (wchar_t)0x004E, (wchar_t)0x004F, (wchar_t)0x0050, (wchar_t)0x0051, (wchar_t)0x0052,
  101  			(wchar_t)0x0053, (wchar_t)0x0054, (wchar_t)0x0055, (wchar_t)0x0056, (wchar_t)0x0057, (wchar_t)0x0058, (wchar_t)0x0059, (wchar_t)0x005A, (wchar_t)0x00C0,
  102  			(wchar_t)0x00C1, (wchar_t)0x00C2, (wchar_t)0x00C3, (wchar_t)0x00C4, (wchar_t)0x00C5, (wchar_t)0x00C6, (wchar_t)0x00C7, (wchar_t)0x00C8, (wchar_t)0x00C9,
  103  			(wchar_t)0x00CA, (wchar_t)0x00CB, (wchar_t)0x00CC, (wchar_t)0x00CD, (wchar_t)0x00CE, (wchar_t)0x00CF, (wchar_t)0x00D0, (wchar_t)0x00D1, (wchar_t)0x00D2,
  104  			(wchar_t)0x00D3, (wchar_t)0x00D4, (wchar_t)0x00D5, (wchar_t)0x00D6, (wchar_t)0x00D8, (wchar_t)0x00D9, (wchar_t)0x00DA, (wchar_t)0x00DB, (wchar_t)0x00DC,
  105  			(wchar_t)0x00DD, (wchar_t)0x00DE, (wchar_t)0x0178, (wchar_t)0x0100, (wchar_t)0x0102, (wchar_t)0x0104, (wchar_t)0x0106, (wchar_t)0x0108, (wchar_t)0x010A,
  106  			(wchar_t)0x010C, (wchar_t)0x010E, (wchar_t)0x0110, (wchar_t)0x0112, (wchar_t)0x0114, (wchar_t)0x0116, (wchar_t)0x0118, (wchar_t)0x011A, (wchar_t)0x011C,
  107  			(wchar_t)0x011E, (wchar_t)0x0120, (wchar_t)0x0122, (wchar_t)0x0124, (wchar_t)0x0126, (wchar_t)0x0128, (wchar_t)0x012A, (wchar_t)0x012C, (wchar_t)0x012E,
  108  			(wchar_t)0x0049, (wchar_t)0x0132, (wchar_t)0x0134, (wchar_t)0x0136, (wchar_t)0x0139, (wchar_t)0x013B, (wchar_t)0x013D, (wchar_t)0x013F, (wchar_t)0x0141,
  109  			(wchar_t)0x0143, (wchar_t)0x0145, (wchar_t)0x0147, (wchar_t)0x014A, (wchar_t)0x014C, (wchar_t)0x014E, (wchar_t)0x0150, (wchar_t)0x0152, (wchar_t)0x0154,
  110  			(wchar_t)0x0156, (wchar_t)0x0158, (wchar_t)0x015A, (wchar_t)0x015C, (wchar_t)0x015E, (wchar_t)0x0160, (wchar_t)0x0162, (wchar_t)0x0164, (wchar_t)0x0166,
  111  			(wchar_t)0x0168, (wchar_t)0x016A, (wchar_t)0x016C, (wchar_t)0x016E, (wchar_t)0x0170, (wchar_t)0x0172, (wchar_t)0x0174, (wchar_t)0x0176, (wchar_t)0x0179,
  112  			(wchar_t)0x017B, (wchar_t)0x017D, (wchar_t)0x0182, (wchar_t)0x0184, (wchar_t)0x0187, (wchar_t)0x018B, (wchar_t)0x0191, (wchar_t)0x0198, (wchar_t)0x01A0,
  113  			(wchar_t)0x01A2, (wchar_t)0x01A4, (wchar_t)0x01A7, (wchar_t)0x01AC, (wchar_t)0x01AF, (wchar_t)0x01B3, (wchar_t)0x01B5, (wchar_t)0x01B8, (wchar_t)0x01BC,
  114  			(wchar_t)0x01C4, (wchar_t)0x01C7, (wchar_t)0x01CA, (wchar_t)0x01CD, (wchar_t)0x01CF, (wchar_t)0x01D1, (wchar_t)0x01D3, (wchar_t)0x01D5, (wchar_t)0x01D7,
  115  			(wchar_t)0x01D9, (wchar_t)0x01DB, (wchar_t)0x01DE, (wchar_t)0x01E0, (wchar_t)0x01E2, (wchar_t)0x01E4, (wchar_t)0x01E6, (wchar_t)0x01E8, (wchar_t)0x01EA,
  116  			(wchar_t)0x01EC, (wchar_t)0x01EE, (wchar_t)0x01F1, (wchar_t)0x01F4, (wchar_t)0x01FA, (wchar_t)0x01FC, (wchar_t)0x01FE, (wchar_t)0x0200, (wchar_t)0x0202,
  117  			(wchar_t)0x0204, (wchar_t)0x0206, (wchar_t)0x0208, (wchar_t)0x020A, (wchar_t)0x020C, (wchar_t)0x020E, (wchar_t)0x0210, (wchar_t)0x0212, (wchar_t)0x0214,
  118  			(wchar_t)0x0216, (wchar_t)0x0181, (wchar_t)0x0186, (wchar_t)0x018A, (wchar_t)0x018E, (wchar_t)0x018F, (wchar_t)0x0190, (wchar_t)0x0193, (wchar_t)0x0194,
  119  			(wchar_t)0x0197, (wchar_t)0x0196, (wchar_t)0x019C, (wchar_t)0x019D, (wchar_t)0x019F, (wchar_t)0x01A9, (wchar_t)0x01AE, (wchar_t)0x01B1, (wchar_t)0x01B2,
  120  			(wchar_t)0x01B7, (wchar_t)0x0386, (wchar_t)0x0388, (wchar_t)0x0389, (wchar_t)0x038A, (wchar_t)0x0391, (wchar_t)0x0392, (wchar_t)0x0393, (wchar_t)0x0394,
  121  			(wchar_t)0x0395, (wchar_t)0x0396, (wchar_t)0x0397, (wchar_t)0x0398, (wchar_t)0x0399, (wchar_t)0x039A, (wchar_t)0x039B, (wchar_t)0x039C, (wchar_t)0x039D,
  122  			(wchar_t)0x039E, (wchar_t)0x039F, (wchar_t)0x03A0, (wchar_t)0x03A1, (wchar_t)0x03A3, (wchar_t)0x03A4, (wchar_t)0x03A5, (wchar_t)0x03A6, (wchar_t)0x03A7,
  123  			(wchar_t)0x03A8, (wchar_t)0x03A9, (wchar_t)0x03AA, (wchar_t)0x03AB, (wchar_t)0x038C, (wchar_t)0x038E, (wchar_t)0x038F, (wchar_t)0x03E2, (wchar_t)0x03E4,
  124  			(wchar_t)0x03E6, (wchar_t)0x03E8, (wchar_t)0x03EA, (wchar_t)0x03EC, (wchar_t)0x03EE, (wchar_t)0x0410, (wchar_t)0x0411, (wchar_t)0x0412, (wchar_t)0x0413,
  125  			(wchar_t)0x0414, (wchar_t)0x0415, (wchar_t)0x0416, (wchar_t)0x0417, (wchar_t)0x0418, (wchar_t)0x0419, (wchar_t)0x041A, (wchar_t)0x041B, (wchar_t)0x041C,
  126  			(wchar_t)0x041D, (wchar_t)0x041E, (wchar_t)0x041F, (wchar_t)0x0420, (wchar_t)0x0421, (wchar_t)0x0422, (wchar_t)0x0423, (wchar_t)0x0424, (wchar_t)0x0425,
  127  			(wchar_t)0x0426, (wchar_t)0x0427, (wchar_t)0x0428, (wchar_t)0x0429, (wchar_t)0x042A, (wchar_t)0x042B, (wchar_t)0x042C, (wchar_t)0x042D, (wchar_t)0x042E,
  128  			(wchar_t)0x042F, (wchar_t)0x0401, (wchar_t)0x0402, (wchar_t)0x0403, (wchar_t)0x0404, (wchar_t)0x0405, (wchar_t)0x0406, (wchar_t)0x0407, (wchar_t)0x0408,
  129  			(wchar_t)0x0409, (wchar_t)0x040A, (wchar_t)0x040B, (wchar_t)0x040C, (wchar_t)0x040E, (wchar_t)0x040F, (wchar_t)0x0460, (wchar_t)0x0462, (wchar_t)0x0464,
  130  			(wchar_t)0x0466, (wchar_t)0x0468, (wchar_t)0x046A, (wchar_t)0x046C, (wchar_t)0x046E, (wchar_t)0x0470, (wchar_t)0x0472, (wchar_t)0x0474, (wchar_t)0x0476,
  131  			(wchar_t)0x0478, (wchar_t)0x047A, (wchar_t)0x047C, (wchar_t)0x047E, (wchar_t)0x0480, (wchar_t)0x0490, (wchar_t)0x0492, (wchar_t)0x0494, (wchar_t)0x0496,
  132  			(wchar_t)0x0498, (wchar_t)0x049A, (wchar_t)0x049C, (wchar_t)0x049E, (wchar_t)0x04A0, (wchar_t)0x04A2, (wchar_t)0x04A4, (wchar_t)0x04A6, (wchar_t)0x04A8,
  133  			(wchar_t)0x04AA, (wchar_t)0x04AC, (wchar_t)0x04AE, (wchar_t)0x04B0, (wchar_t)0x04B2, (wchar_t)0x04B4, (wchar_t)0x04B6, (wchar_t)0x04B8, (wchar_t)0x04BA,
  134  			(wchar_t)0x04BC, (wchar_t)0x04BE, (wchar_t)0x04C1, (wchar_t)0x04C3, (wchar_t)0x04C7, (wchar_t)0x04CB, (wchar_t)0x04D0, (wchar_t)0x04D2, (wchar_t)0x04D4,
  135  			(wchar_t)0x04D6, (wchar_t)0x04D8, (wchar_t)0x04DA, (wchar_t)0x04DC, (wchar_t)0x04DE, (wchar_t)0x04E0, (wchar_t)0x04E2, (wchar_t)0x04E4, (wchar_t)0x04E6,
  136  			(wchar_t)0x04E8, (wchar_t)0x04EA, (wchar_t)0x04EE, (wchar_t)0x04F0, (wchar_t)0x04F2, (wchar_t)0x04F4, (wchar_t)0x04F8, (wchar_t)0x0531, (wchar_t)0x0532,
  137  			(wchar_t)0x0533, (wchar_t)0x0534, (wchar_t)0x0535, (wchar_t)0x0536, (wchar_t)0x0537, (wchar_t)0x0538, (wchar_t)0x0539, (wchar_t)0x053A, (wchar_t)0x053B,
  138  			(wchar_t)0x053C, (wchar_t)0x053D, (wchar_t)0x053E, (wchar_t)0x053F, (wchar_t)0x0540, (wchar_t)0x0541, (wchar_t)0x0542, (wchar_t)0x0543, (wchar_t)0x0544,
  139  			(wchar_t)0x0545, (wchar_t)0x0546, (wchar_t)0x0547, (wchar_t)0x0548, (wchar_t)0x0549, (wchar_t)0x054A, (wchar_t)0x054B, (wchar_t)0x054C, (wchar_t)0x054D,
  140  			(wchar_t)0x054E, (wchar_t)0x054F, (wchar_t)0x0550, (wchar_t)0x0551, (wchar_t)0x0552, (wchar_t)0x0553, (wchar_t)0x0554, (wchar_t)0x0555, (wchar_t)0x0556,
  141  			(wchar_t)0x10A0, (wchar_t)0x10A1, (wchar_t)0x10A2, (wchar_t)0x10A3, (wchar_t)0x10A4, (wchar_t)0x10A5, (wchar_t)0x10A6, (wchar_t)0x10A7, (wchar_t)0x10A8,
  142  			(wchar_t)0x10A9, (wchar_t)0x10AA, (wchar_t)0x10AB, (wchar_t)0x10AC, (wchar_t)0x10AD, (wchar_t)0x10AE, (wchar_t)0x10AF, (wchar_t)0x10B0, (wchar_t)0x10B1,
  143  			(wchar_t)0x10B2, (wchar_t)0x10B3, (wchar_t)0x10B4, (wchar_t)0x10B5, (wchar_t)0x10B6, (wchar_t)0x10B7, (wchar_t)0x10B8, (wchar_t)0x10B9, (wchar_t)0x10BA,
  144  			(wchar_t)0x10BB, (wchar_t)0x10BC, (wchar_t)0x10BD, (wchar_t)0x10BE, (wchar_t)0x10BF, (wchar_t)0x10C0, (wchar_t)0x10C1, (wchar_t)0x10C2, (wchar_t)0x10C3,
  145  			(wchar_t)0x10C4, (wchar_t)0x10C5, (wchar_t)0x1E00, (wchar_t)0x1E02, (wchar_t)0x1E04, (wchar_t)0x1E06, (wchar_t)0x1E08, (wchar_t)0x1E0A, (wchar_t)0x1E0C,
  146  			(wchar_t)0x1E0E, (wchar_t)0x1E10, (wchar_t)0x1E12, (wchar_t)0x1E14, (wchar_t)0x1E16, (wchar_t)0x1E18, (wchar_t)0x1E1A, (wchar_t)0x1E1C, (wchar_t)0x1E1E,
  147  			(wchar_t)0x1E20, (wchar_t)0x1E22, (wchar_t)0x1E24, (wchar_t)0x1E26, (wchar_t)0x1E28, (wchar_t)0x1E2A, (wchar_t)0x1E2C, (wchar_t)0x1E2E, (wchar_t)0x1E30,
  148  			(wchar_t)0x1E32, (wchar_t)0x1E34, (wchar_t)0x1E36, (wchar_t)0x1E38, (wchar_t)0x1E3A, (wchar_t)0x1E3C, (wchar_t)0x1E3E, (wchar_t)0x1E40, (wchar_t)0x1E42,
  149  			(wchar_t)0x1E44, (wchar_t)0x1E46, (wchar_t)0x1E48, (wchar_t)0x1E4A, (wchar_t)0x1E4C, (wchar_t)0x1E4E, (wchar_t)0x1E50, (wchar_t)0x1E52, (wchar_t)0x1E54,
  150  			(wchar_t)0x1E56, (wchar_t)0x1E58, (wchar_t)0x1E5A, (wchar_t)0x1E5C, (wchar_t)0x1E5E, (wchar_t)0x1E60, (wchar_t)0x1E62, (wchar_t)0x1E64, (wchar_t)0x1E66,
  151  			(wchar_t)0x1E68, (wchar_t)0x1E6A, (wchar_t)0x1E6C, (wchar_t)0x1E6E, (wchar_t)0x1E70, (wchar_t)0x1E72, (wchar_t)0x1E74, (wchar_t)0x1E76, (wchar_t)0x1E78,
  152  			(wchar_t)0x1E7A, (wchar_t)0x1E7C, (wchar_t)0x1E7E, (wchar_t)0x1E80, (wchar_t)0x1E82, (wchar_t)0x1E84, (wchar_t)0x1E86, (wchar_t)0x1E88, (wchar_t)0x1E8A,
  153  			(wchar_t)0x1E8C, (wchar_t)0x1E8E, (wchar_t)0x1E90, (wchar_t)0x1E92, (wchar_t)0x1E94, (wchar_t)0x1EA0, (wchar_t)0x1EA2, (wchar_t)0x1EA4, (wchar_t)0x1EA6,
  154  			(wchar_t)0x1EA8, (wchar_t)0x1EAA, (wchar_t)0x1EAC, (wchar_t)0x1EAE, (wchar_t)0x1EB0, (wchar_t)0x1EB2, (wchar_t)0x1EB4, (wchar_t)0x1EB6, (wchar_t)0x1EB8,
  155  			(wchar_t)0x1EBA, (wchar_t)0x1EBC, (wchar_t)0x1EBE, (wchar_t)0x1EC0, (wchar_t)0x1EC2, (wchar_t)0x1EC4, (wchar_t)0x1EC6, (wchar_t)0x1EC8, (wchar_t)0x1ECA,
  156  			(wchar_t)0x1ECC, (wchar_t)0x1ECE, (wchar_t)0x1ED0, (wchar_t)0x1ED2, (wchar_t)0x1ED4, (wchar_t)0x1ED6, (wchar_t)0x1ED8, (wchar_t)0x1EDA, (wchar_t)0x1EDC,
  157  			(wchar_t)0x1EDE, (wchar_t)0x1EE0, (wchar_t)0x1EE2, (wchar_t)0x1EE4, (wchar_t)0x1EE6, (wchar_t)0x1EE8, (wchar_t)0x1EEA, (wchar_t)0x1EEC, (wchar_t)0x1EEE,
  158  			(wchar_t)0x1EF0, (wchar_t)0x1EF2, (wchar_t)0x1EF4, (wchar_t)0x1EF6, (wchar_t)0x1EF8, (wchar_t)0x1F08, (wchar_t)0x1F09, (wchar_t)0x1F0A, (wchar_t)0x1F0B,
  159  			(wchar_t)0x1F0C, (wchar_t)0x1F0D, (wchar_t)0x1F0E, (wchar_t)0x1F0F, (wchar_t)0x1F18, (wchar_t)0x1F19, (wchar_t)0x1F1A, (wchar_t)0x1F1B, (wchar_t)0x1F1C,
  160  			(wchar_t)0x1F1D, (wchar_t)0x1F28, (wchar_t)0x1F29, (wchar_t)0x1F2A, (wchar_t)0x1F2B, (wchar_t)0x1F2C, (wchar_t)0x1F2D, (wchar_t)0x1F2E, (wchar_t)0x1F2F,
  161  			(wchar_t)0x1F38, (wchar_t)0x1F39, (wchar_t)0x1F3A, (wchar_t)0x1F3B, (wchar_t)0x1F3C, (wchar_t)0x1F3D, (wchar_t)0x1F3E, (wchar_t)0x1F3F, (wchar_t)0x1F48,
  162  			(wchar_t)0x1F49, (wchar_t)0x1F4A, (wchar_t)0x1F4B, (wchar_t)0x1F4C, (wchar_t)0x1F4D, (wchar_t)0x1F59, (wchar_t)0x1F5B, (wchar_t)0x1F5D, (wchar_t)0x1F5F,
  163  			(wchar_t)0x1F68, (wchar_t)0x1F69, (wchar_t)0x1F6A, (wchar_t)0x1F6B, (wchar_t)0x1F6C, (wchar_t)0x1F6D, (wchar_t)0x1F6E, (wchar_t)0x1F6F, (wchar_t)0x1F88,
  164  			(wchar_t)0x1F89, (wchar_t)0x1F8A, (wchar_t)0x1F8B, (wchar_t)0x1F8C, (wchar_t)0x1F8D, (wchar_t)0x1F8E, (wchar_t)0x1F8F, (wchar_t)0x1F98, (wchar_t)0x1F99,
  165  			(wchar_t)0x1F9A, (wchar_t)0x1F9B, (wchar_t)0x1F9C, (wchar_t)0x1F9D, (wchar_t)0x1F9E, (wchar_t)0x1F9F, (wchar_t)0x1FA8, (wchar_t)0x1FA9, (wchar_t)0x1FAA,
  166  			(wchar_t)0x1FAB, (wchar_t)0x1FAC, (wchar_t)0x1FAD, (wchar_t)0x1FAE, (wchar_t)0x1FAF, (wchar_t)0x1FB8, (wchar_t)0x1FB9, (wchar_t)0x1FD8, (wchar_t)0x1FD9,
  167  			(wchar_t)0x1FE8, (wchar_t)0x1FE9, (wchar_t)0x24B6, (wchar_t)0x24B7, (wchar_t)0x24B8, (wchar_t)0x24B9, (wchar_t)0x24BA, (wchar_t)0x24BB, (wchar_t)0x24BC,
  168  			(wchar_t)0x24BD, (wchar_t)0x24BE, (wchar_t)0x24BF, (wchar_t)0x24C0, (wchar_t)0x24C1, (wchar_t)0x24C2, (wchar_t)0x24C3, (wchar_t)0x24C4, (wchar_t)0x24C5,
  169  			(wchar_t)0x24C6, (wchar_t)0x24C7, (wchar_t)0x24C8, (wchar_t)0x24C9, (wchar_t)0x24CA, (wchar_t)0x24CB, (wchar_t)0x24CC, (wchar_t)0x24CD, (wchar_t)0x24CE,
  170  			(wchar_t)0x24CF, (wchar_t)0xFF21, (wchar_t)0xFF22, (wchar_t)0xFF23, (wchar_t)0xFF24, (wchar_t)0xFF25, (wchar_t)0xFF26, (wchar_t)0xFF27, (wchar_t)0xFF28,
  171  			(wchar_t)0xFF29, (wchar_t)0xFF2A, (wchar_t)0xFF2B, (wchar_t)0xFF2C, (wchar_t)0xFF2D, (wchar_t)0xFF2E, (wchar_t)0xFF2F, (wchar_t)0xFF30, (wchar_t)0xFF31,
  172  			(wchar_t)0xFF32, (wchar_t)0xFF33, (wchar_t)0xFF34, (wchar_t)0xFF35, (wchar_t)0xFF36, (wchar_t)0xFF37, (wchar_t)0xFF38, (wchar_t)0xFF39, (wchar_t)0xFF3A };
  173  
  174  		static int compareWchar(const void* a, const void* b)
  175  		{
  176  			if (*(wchar_t*)a < *(wchar_t*)b)
  177  				return -1;
  178  			else if (*(wchar_t*)a > *(wchar_t*)b)
  179  				return 1;
  180  
  181  			return 0;
  182  		}
  183  
  184  		static  wchar_t tolowerUnicode(const wchar_t& c)
  185  		{
  186  			wchar_t* p = (wchar_t*)bsearch(&c, unicode_uppers, sizeof(unicode_uppers) / sizeof(wchar_t), sizeof(wchar_t), compareWchar);
  187  			if (p)
  188  				return *(unicode_lowers + (p - unicode_uppers));
  189  
  190  			return c;
  191  		}
  192  
  193  		static wchar_t toupperUnicode(const wchar_t& c)
  194  		{
  195  			wchar_t* p = (wchar_t*)bsearch(&c, unicode_lowers, sizeof(unicode_lowers) / sizeof(wchar_t), sizeof(wchar_t), compareWchar);
  196  			if (p)
  197  				return *(unicode_uppers + (p - unicode_lowers));
  198  
  199  			return c;
  200  		}
  201  
  202  		unsigned int chars2Unicode(const std::string& _string, size_t& _cursor)
  203  		{
  204  			unsigned const char checkCharType = _string[_cursor];
  205  			unsigned int result = '?';
  206  
  207  			// 0xxxxxxx, one byte character.
  208  			if (checkCharType <= 0x7F) {
  209  				// 0xxxxxxx
  210  				result = (_string[_cursor++]);
  211  			}
  212  			// 11110xxx, four byte character.
  213  			else if (checkCharType >= 0xF0 && _cursor < _string.length() - 2) {
  214  				// 11110xxx 10xxxxxx 10xxxxxx 10xxxxxx
  215  				result = (_string[_cursor++] & 0x07) << 18;
  216  				result |= (_string[_cursor++] & 0x3F) << 12;
  217  				result |= (_string[_cursor++] & 0x3F) << 6;
  218  				result |= _string[_cursor++] & 0x3F;
  219  			}
  220  			// 1110xxxx, three byte character.
  221  			else if (checkCharType >= 0xE0 && _cursor < _string.length() - 1) {
  222  				// 1110xxxx 10xxxxxx 10xxxxxx
  223  				result = (_string[_cursor++] & 0x0F) << 12;
  224  				result |= (_string[_cursor++] & 0x3F) << 6;
  225  				result |= _string[_cursor++] & 0x3F;
  226  			}
  227  			// 110xxxxx, two byte character.
  228  			else if (checkCharType >= 0xC0 && _cursor < _string.length()) {
  229  				// 110xxxxx 10xxxxxx
  230  				result = (_string[_cursor++] & 0x1F) << 6;
  231  				result |= _string[_cursor++] & 0x3F;
  232  			}
  233  			else {
  234  				// Error, invalid character.
  235  				++_cursor;
  236  			}
  237  
  238  			return result;
  239  
  240  		} // chars2Unicode
  241  
  242  		std::string unicode2Chars(const unsigned int _unicode)
  243  		{
  244  			std::string result;
  245  
  246  			if(_unicode < 0x80) // one byte character
  247  			{
  248  				result += ((_unicode      ) & 0xFF);
  249  			}
  250  			else if(_unicode < 0x800) // two byte character
  251  			{
  252  				result += ((_unicode >>  6) & 0xFF) | 0xC0;
  253  				result += ((_unicode      ) & 0x3F) | 0x80;
  254  			}
  255  			else if(_unicode < 0xFFFF) // three byte character
  256  			{
  257  				result += ((_unicode >> 12) & 0xFF) | 0xE0;
  258  				result += ((_unicode >>  6) & 0x3F) | 0x80;
  259  				result += ((_unicode      ) & 0x3F) | 0x80;
  260  			}
  261  			else if(_unicode <= 0x1fffff) // four byte character
  262  			{
  263  				result += ((_unicode >> 18) & 0xFF) | 0xF0;
  264  				result += ((_unicode >> 12) & 0x3F) | 0x80;
  265  				result += ((_unicode >>  6) & 0x3F) | 0x80;
  266  				result += ((_unicode      ) & 0x3F) | 0x80;
  267  			}
  268  			else
  269  			{
  270  				// error, invalid unicode
  271  				result += '?';
  272  			}
  273  
  274  			return result;
  275  
  276  		} // unicode2Chars
  277  
  278  		size_t nextCursor(const std::string& _string, const size_t _cursor)
  279  		{
  280  			size_t result = _cursor;
  281  
  282  			while(result < _string.length())
  283  			{
  284  				++result;
  285  
  286  				if((_string[result] & 0xC0) != 0x80) // break if current character is not 10xxxxxx
  287  					break;
  288  			}
  289  
  290  			return result;
  291  
  292  		} // nextCursor
  293  
  294  		size_t prevCursor(const std::string& _string, const size_t _cursor)
  295  		{
  296  			size_t result = _cursor;
  297  
  298  			while(result > 0)
  299  			{
  300  				--result;
  301  
  302  				if((_string[result] & 0xC0) != 0x80) // break if current character is not 10xxxxxx
  303  					break;
  304  			}
  305  
  306  			return result;
  307  
  308  		} // prevCursor
  309  
  310  		size_t moveCursor(const std::string& _string, const size_t _cursor, const int _amount)
  311  		{
  312  			size_t result = _cursor;
  313  
  314  			if(_amount > 0)
  315  			{
  316  				for(int i = 0; i < _amount; ++i)
  317  					result = nextCursor(_string, result);
  318  			}
  319  			else if(_amount < 0)
  320  			{
  321  				for(int i = _amount; i < 0; ++i)
  322  					result = prevCursor(_string, result);
  323  			}
  324  
  325  			return result;
  326  
  327  		} // moveCursor
  328  		
  329  		std::string toLower(const std::string& _string) 
  330  		{
  331  			std::string text = _string;
  332  
  333  			size_t i = 0;
  334  			while (i < text.length())
  335  			{
  336  				char c = text[i];
  337  				if ((c & 0x80) == 0)
  338  				{
  339  					if (c >= 'A' && c <= 'Z')
  340  						text[i] = c + 0x20;
  341  
  342  					i++;
  343  					continue;
  344  				}
  345  
  346  				int pos = i;
  347  				wchar_t character = (wchar_t)chars2Unicode(text, i);
  348  				wchar_t unicode = tolowerUnicode(character);
  349  				if (unicode != character)
  350  				{
  351  					int charSize = i - pos;
  352  					if (charSize == 2)
  353  					{
  354  						text[pos] = (char)(((unicode >> 6) & 0xFF) | 0xC0);
  355  						text[pos + 1] = (char)((unicode & 0x3F) | 0x80);
  356  					}
  357  					else if (charSize == 3)
  358  					{
  359  						text[pos] += (char)(((unicode >> 12) & 0xFF) | 0xE0);
  360  						text[pos + 1] += (char)(((unicode >> 6) & 0x3F) | 0x80);
  361  						text[pos + 2] += (char)((unicode & 0x3F) | 0x80);
  362  
  363  					}
  364  				}
  365  			}
  366  
  367  			return text;
  368  		}
  369  
  370  		std::string toUpper(const std::string& _string) 
  371  		{
  372  			std::string text = _string;
  373  
  374  			size_t i = 0;
  375  			while (i < text.length())
  376  			{
  377  				char c = text[i];
  378  				if ((c & 0x80) == 0)
  379  				{
  380  					if (c >= 'a' && c <= 'z')
  381  						text[i] = c - 0x20;
  382  
  383  					i++;
  384  					continue;
  385  				}
  386  
  387  				int pos = i;
  388  				wchar_t character = (wchar_t)chars2Unicode(text, i);
  389  				wchar_t unicode = toupperUnicode(character);
  390  				if (unicode != character)
  391  				{
  392  					int charSize = i - pos;
  393  					if (charSize == 2)
  394  					{
  395  						text[pos] = (char)(((unicode >> 6) & 0xFF) | 0xC0);
  396  						text[pos + 1] = (char)((unicode & 0x3F) | 0x80);
  397  					}
  398  					else if (charSize == 3)
  399  					{
  400  						text[pos] += (char)(((unicode >> 12) & 0xFF) | 0xE0);
  401  						text[pos + 1] += (char)(((unicode >> 6) & 0x3F) | 0x80);
  402  						text[pos + 2] += (char)((unicode & 0x3F) | 0x80);
  403  					}
  404  				}
  405  			}
  406  
  407  			return text;
  408  		}
  409  
  410  		std::string trim(const std::string& _string)
  411  		{
  412  			const size_t strBegin = _string.find_first_not_of(" \t\r\n");
  413  			if(strBegin == std::string::npos)
  414  				return "";
  415  
  416  			const size_t strEnd = _string.find_last_not_of(" \t\r\n");		
  417  
  418  			const size_t len = strEnd - strBegin + 1;
  419  			if (strBegin == 0 && len == _string.length())
  420  				return _string;
  421  
  422  			return _string.substr(strBegin, strEnd - strBegin + 1);
  423  
  424  		} // trim
  425  
  426  		std::string shellQuote(const std::string& _string)
  427  		{
  428  			// Wrap the value in single quotes so it reaches the command as one
  429  			// literal argument. Inside single quotes the shell expands nothing,
  430  			// so $, `, \, " and whitespace survive untouched; a single quote
  431  			// itself has to leave the quoted run, be escaped, and re-enter it.
  432  			std::string quoted = "'";
  433  
  434  			for (auto character : _string)
  435  			{
  436  				if (character == '\'')
  437  					quoted += "'\\''";
  438  				else
  439  					quoted += character;
  440  			}
  441  
  442  			return quoted + "'";
  443  
  444  		} // shellQuote
  445  
  446  		// ------------------------------------------------------------ maskSecrets
  447  		//
  448  		// A credential's value never reaches a log (D-INFRA-011): every command
  449  		// line, URL or query EmulationStation logs goes through here first, at
  450  		// every level (fork #177). The key or flag stays and the value reads
  451  		// <redacted>, so the line still says what ran; an empty value stays
  452  		// empty, since whether a credential is set may be shown and only what it
  453  		// is may not. A value already written as a placeholder in angle brackets
  454  		// (<password>, <redacted>) is left alone, which also makes a second pass
  455  		// a no-op.
  456  		//
  457  		// What counts as a credential's value, in the shapes this tree builds:
  458  		//
  459  		//   setrootpass hunter2                the rest of the line: GuiMenu quotes
  460  		//                                      the password since #198, and a log line
  461  		//                                      from before it, or a hand-typed one, has
  462  		//                                      it bare -- either way no tail is left
  463  		//   wifictl connect 'ssid' 'psk' 'CC'  the second word after connect or
  464  		//   wifictl enable 'ssid' 'psk'        enable: the passphrase, not the SSID
  465  		//   --password x, -p x, -pin x,        a flag ending in a credential word,
  466  		//   -netplaypass x, --token x          then one word; --key is batocera-
  467  		//                                      hotkeys' key NAME and mkdir -p takes
  468  		//                                      no value, so neither masks
  469  		//   password=x, pass=x, token=x,       a name ending in a credential word,
  470  		//   key=x, secret=x, psk=x, pin=x      then =: devpassword, cheevos_token,
  471  		//                                      wifi.key, ScreenScraperPass, api-key
  472  		//   ?y=x, &t=x, &p=x                   RetroAchievements' one-letter query
  473  		//                                      keys: the web API key, the token,
  474  		//                                      the login password
  475  		//
  476  		// A value is one shell word: every single-quoted, double-quoted and bare
  477  		// piece of it and every backslash-escaped character, to the next
  478  		// unquoted space, &, ; or | (#308 F-ES-09) -- shellQuote's '\'' escape
  479  		// is three such pieces. The quotes go with the value, so a passphrase
  480  		// with spaces is masked whole. Inside a quoted string (a URL in double
  481  		// quotes) the value ends at that string's closing quote. An unterminated
  482  		// quote takes the rest of the line: where the shape is unclear, more is
  483  		// masked rather than less.
  484  
  485  		static bool maskIsWordChar(char c)
  486  		{
  487  			return (c >= 'a' && c <= 'z') || (c >= 'A' && c <= 'Z') || (c >= '0' && c <= '9')
  488  				|| c == '_' || c == '.' || c == '-';
  489  		}
  490  
  491  		static bool maskIsSpace(char c)
  492  		{
  493  			return c == ' ' || c == '\t' || c == '\r' || c == '\n';
  494  		}
  495  
  496  		static bool maskEndsValue(char c)
  497  		{
  498  			return maskIsSpace(c) || c == '&' || c == ';' || c == '|' || c == '\'' || c == '"';
  499  		}
  500  
  501  		static std::string maskLower(const std::string& word)
  502  		{
  503  			std::string lower = word;
  504  			for (auto& c : lower)
  505  				if (c >= 'A' && c <= 'Z')
  506  					c = (char)(c - 'A' + 'a');
  507  			return lower;
  508  		}
  509  
  510  		// Does a lower-cased name end in a word that means "credential"?
  511  		static bool maskIsSecretName(const std::string& lower)
  512  		{
  513  			static const char* const words[] = { "password", "pass", "token", "key", "secret", "psk", "pin" };
  514  			for (const char* word : words)
  515  			{
  516  				const size_t len = strlen(word);
  517  				if (lower.size() >= len && lower.compare(lower.size() - len, len, word) == 0)
  518  					return true;
  519  			}
  520  			return false;
  521  		}
  522  
  523  		// What quote `pos` sits inside, reading the line from its start as the
  524  		// shell would: 0 at the top level, else the quote character.
  525  		static char maskQuoteAt(const std::string& s, size_t pos)
  526  		{
  527  			char quote = 0;
  528  			for (size_t i = 0; i < pos && i < s.size(); ++i)
  529  			{
  530  				const char c = s[i];
  531  				if (quote == '\'')
  532  				{
  533  					if (c == '\'')
  534  						quote = 0;
  535  					continue;
  536  				}
  537  				if (c == '\\')
  538  				{
  539  					++i;
  540  					continue;
  541  				}
  542  				if (quote == '"')
  543  				{
  544  					if (c == '"')
  545  						quote = 0;
  546  					continue;
  547  				}
  548  				if (c == '\'' || c == '"')
  549  					quote = c;
  550  			}
  551  			return quote;
  552  		}
  553  
  554  		// One character of the command a quoted string holds, as the shell
  555  		// that runs it will read it (audit of the fix round PL-010): in a
  556  		// double-quoted string \" \\ \$ and \` are one character, the escaped
  557  		// one, and any other backslash stays itself; in a single-quoted string
  558  		// every byte stands for itself, except shellQuote's '\'' -- close,
  559  		// escaped quote, reopen -- which is one single quote of the command
  560  		// (audit of the fix round, claude G2-E-core-01: a value shellQuote
  561  		// quoted inside a command it quoted again began with that quote, was
  562  		// taken for the string's end, and went to the log unmasked). Sets c,
  563  		// and returns the character's width in the line -- or 0 where the
  564  		// enclosing string itself ends.
  565  		static size_t maskInnerChar(const std::string& s, size_t i, char enclosing, char& c)
  566  		{
  567  			c = s[i];
  568  			if (c == enclosing)
  569  			{
  570  				// The two ways a shell writes a single quote inside a
  571  				// single-quoted string: '\'' and '"'"' (the audit of the
  572  				// fixes, gpt G3-E-01: the second read as the string's end,
  573  				// and the password after it was logged).
  574  				if (enclosing != '\'')
  575  					return 0;
  576  				if (s.compare(i, 4, "'\\''") == 0)
  577  					return 4;
  578  				if (s.compare(i, 5, "'\"'\"'") == 0)
  579  					return 5;
  580  				return 0;
  581  			}
  582  			if (enclosing == '"' && c == '\\' && i + 1 < s.size())
  583  			{
  584  				const char next = s[i + 1];
  585  				if (next == '"' || next == '\\' || next == '$' || next == '`')
  586  				{
  587  					c = next;
  588  					return 2;
  589  				}
  590  			}
  591  			return 1;
  592  		}
  593  
  594  		// The end of the one shell word starting at pos (#308 F-ES-09). At the
  595  		// top level a word runs across every quoted and bare piece of it, and
  596  		// every backslash-escaped character, until unquoted whitespace or &, ;
  597  		// or |: `--password 'front'back` passes the shell frontback, and the
  598  		// mask used to stop at the first closing quote and log "back". Inside
  599  		// a quoted string -- a URL in double quotes, a command in single ones
  600  		// -- the value ends where it always did: at the string's own closing
  601  		// quote, or at whitespace, &, ; or |.
  602  		static size_t maskValueEnd(const std::string& s, size_t pos)
  603  		{
  604  			if (pos >= s.size())
  605  				return pos;
  606  
  607  			// Inside a quoted string -- the command of an sh -c, a URL -- the
  608  			// value is a word of the command the string holds: the string's
  609  			// own closing quote ends it, and so does the inner command's
  610  			// unquoted whitespace, &, ; or |, but the inner command's own quotes
  611  			// keep a word whole. They used to end it before it began, and
  612  			// `sh -c 'tool --password "front back"'` logged the password
  613  			// (audit of the fixes of #307, gpt's coverage note on F-ES-09).
  614  			// The inner command is read character by character as its own shell
  615  			// reads it (maskInnerChar), so a backslash there -- at its top level
  616  			// or inside its double quote -- takes the next character with it:
  617  			// the inner quote was tracked before the backslash, and
  618  			// `sh -c 'tool --password "front\" back"'` logged "back" (audit of
  619  			// the fix round PL-010). Inside the inner single quote a backslash
  620  			// is only a backslash, as the shell has it.
  621  			const char enclosing = maskQuoteAt(s, pos);
  622  			if (enclosing != 0)
  623  			{
  624  				char inner = 0;
  625  				size_t i = pos;
  626  				while (i < s.size())
  627  				{
  628  					char c = 0;
  629  					const size_t width = maskInnerChar(s, i, enclosing, c);
  630  					if (width == 0)
  631  						return i; // the string itself ends
  632  					if (inner == 0 && (maskIsSpace(c) || c == '&' || c == ';' || c == '|'))
  633  						return i;
  634  					i += width;
  635  					if (inner == '\'')
  636  					{
  637  						if (c == '\'')
  638  							inner = 0;
  639  					}
  640  					else if (c == '\\')
  641  					{
  642  						if (i < s.size())
  643  						{
  644  							char escaped = 0;
  645  							const size_t next = maskInnerChar(s, i, enclosing, escaped);
  646  							if (next == 0)
  647  								return i; // the string ends after a lone backslash
  648  							i += next; // the inner command's escaped character
  649  						}
  650  					}
  651  					else if (inner == '"')
  652  					{
  653  						if (c == '"')
  654  							inner = 0;
  655  					}
  656  					else if (c == '\'' || c == '"')
  657  						inner = c;
  658  				}
  659  				return s.size();
  660  			}
  661  
  662  			char quote = 0;
  663  			size_t i = pos;
  664  			for (; i < s.size(); ++i)
  665  			{
  666  				const char c = s[i];
  667  				if (quote == '\'')
  668  				{
  669  					if (c == '\'')
  670  						quote = 0;
  671  					continue;
  672  				}
  673  				if (c == '\\')
  674  				{
  675  					++i; // an escaped character, whatever it is
  676  					continue;
  677  				}
  678  				if (quote == '"')
  679  				{
  680  					if (c == '"')
  681  						quote = 0;
  682  					continue;
  683  				}
  684  				if (c == '\'' || c == '"')
  685  					quote = c;
  686  				else if (maskIsSpace(c) || c == '&' || c == ';' || c == '|')
  687  					return i;
  688  			}
  689  			return s.size(); // the end of the line, or an unterminated quote: the value is the rest
  690  		}
  691  
  692  		static bool maskIsPlaceholder(const std::string& s, size_t pos, size_t end)
  693  		{
  694  			return end > pos + 1 && s[pos] == '<' && s[end - 1] == '>';
  695  		}
  696  
  697  		// Append the value at [pos, end) masked -- or as it is when it is empty
  698  		// or already a placeholder -- and return end.
  699  		static size_t maskAppendValue(const std::string& s, size_t pos, size_t end, std::string& out)
  700  		{
  701  			if (end == pos || maskIsPlaceholder(s, pos, end))
  702  				out.append(s, pos, end - pos);
  703  			else
  704  				out += "<redacted>";
  705  			return end;
  706  		}
  707  
  708  		static size_t maskCopySpaces(const std::string& s, size_t pos, std::string& out)
  709  		{
  710  			while (pos < s.size() && maskIsSpace(s[pos]))
  711  				out += s[pos++];
  712  			return pos;
  713  		}
  714  
  715  		std::string maskSecrets(const std::string& _string)
  716  		{
  717  			const std::string& s = _string;
  718  			std::string out;
  719  			out.reserve(s.size());
  720  
  721  			std::string previous; // the word before this one, lower-cased
  722  			size_t i = 0;
  723  			while (i < s.size())
  724  			{
  725  				if (!maskIsWordChar(s[i]))
  726  				{
  727  					out += s[i++];
  728  					continue;
  729  				}
  730  
  731  				const size_t start = i;
  732  				while (i < s.size() && maskIsWordChar(s[i]))
  733  					++i;
  734  
  735  				const std::string word = maskLower(s.substr(start, i - start));
  736  				out.append(s, start, i - start);
  737  
  738  				// name=value, or a one-letter RetroAchievements key after ? or &
  739  				const bool queryKey = (word == "y" || word == "t" || word == "p")
  740  					&& start > 0 && (s[start - 1] == '?' || s[start - 1] == '&');
  741  
  742  				if (i < s.size() && s[i] == '=' && (queryKey || maskIsSecretName(word)))
  743  				{
  744  					out += '=';
  745  					++i;
  746  					i = maskAppendValue(s, i, maskValueEnd(s, i), out);
  747  					previous = word;
  748  					continue;
  749  				}
  750  
  751  				if (i < s.size() && maskIsSpace(s[i]))
  752  				{
  753  					if (word == "setrootpass")
  754  					{
  755  						i = maskCopySpaces(s, i, out);
  756  						size_t end = s.size();
  757  						while (end > i && maskIsSpace(s[end - 1]))
  758  							--end;
  759  						i = maskAppendValue(s, i, end, out);
  760  						previous = word;
  761  						continue;
  762  					}
  763  
  764  					if (word == "wifictl")
  765  					{
  766  						size_t j = i;
  767  						while (j < s.size() && maskIsSpace(s[j]))
  768  							++j;
  769  						size_t k = j;
  770  						while (k < s.size() && maskIsWordChar(s[k]))
  771  							++k;
  772  
  773  						const std::string sub = maskLower(s.substr(j, k - j));
  774  						if (sub == "connect" || sub == "enable")
  775  						{
  776  							out.append(s, i, k - i);
  777  							i = maskCopySpaces(s, k, out);
  778  							const size_t ssidEnd = maskValueEnd(s, i); // the SSID is no secret
  779  							out.append(s, i, ssidEnd - i);
  780  							i = maskCopySpaces(s, ssidEnd, out);
  781  							i = maskAppendValue(s, i, maskValueEnd(s, i), out);
  782  							previous = sub;
  783  							continue;
  784  						}
  785  					}
  786  
  787  					const bool flag = word.size() > 1 && word[0] == '-'
  788  						&& ((word == "-p" && previous != "mkdir") || (word != "--key" && maskIsSecretName(word)));
  789  					if (flag)
  790  					{
  791  						i = maskCopySpaces(s, i, out);
  792  						i = maskAppendValue(s, i, maskValueEnd(s, i), out);
  793  						previous = word;
  794  						continue;
  795  					}
  796  				}
  797  
  798  				previous = word;
  799  			}
  800  
  801  			return out;
  802  
  803  		} // maskSecrets
  804  
  805  		std::string replace(const std::string& _string, const std::string& _replace, const std::string& _with)
  806  		{
  807  			if (_replace.empty())
  808  				return _string;
  809  
  810  			std::string string = _string;
  811  			
  812  			size_t pos = 0;
  813  			while ((pos = string.find(_replace, pos)) != std::string::npos) {
  814  				string = string.replace(pos, _replace.length(), _with.c_str());
  815  				pos += _with.length();
  816  			}
  817  			
  818  			return string;
  819  
  820  		} // replace
  821  
  822  		bool startsWith(const std::string& _string, const std::string& _start)
  823  		{
  824  			return (strncmp(_string.c_str(), _start.c_str(), _start.size()) == 0);
  825  		} // startsWith
  826  
  827  		bool endsWith(const std::string& _string, const std::string& _end)
  828  		{
  829  			if (_end.size() > _string.size()) return false;
  830  			return (_string.rfind(_end) == (_string.size() - _end.size()));
  831  		} // endsWith
  832  
  833  		std::string removeParenthesis(const std::string& _string)
  834  		{
  835  			static const char remove[4] = { '(', ')', '[', ']' };
  836  			std::string       string = _string;
  837  			size_t            start;
  838  			size_t            end;
  839  			bool              done = false;
  840  
  841  			while(!done)
  842  			{
  843  				done = true;
  844  
  845  				for(int i = 0; i < sizeof(remove); i += 2)
  846  				{
  847  					end   = string.find_first_of(remove[i + 1]);
  848  					start = string.find_last_of( remove[i + 0], end);
  849  
  850  					if((start != std::string::npos) && (end != std::string::npos))
  851  					{
  852  						string.erase(start, end - start + 1);
  853  						done = false;
  854  					}
  855  				}
  856  			}
  857  
  858  			return trim(string);
  859  
  860  		} // removeParenthesis
  861  
  862  		std::string vectorToCommaString(stringVector _vector)
  863  		{
  864  			std::string string;
  865  
  866  			std::sort(_vector.begin(), _vector.end());
  867  
  868  			for(stringVector::const_iterator it = _vector.cbegin(); it != _vector.cend(); ++it)
  869  				string += (string.length() ? "," : "") + (*it);
  870  
  871  			return string;
  872  
  873  		} // vectorToCommaString
  874  
  875  		stringVector commaStringToVector(const std::string& _string)
  876  		{
  877  			return Utils::String::split(_string, ',', false);
  878  		}
  879  
  880  		std::string format(const char* _format, ...)
  881  		{
  882  			va_list	args;
  883  			va_list copy;
  884  
  885  			va_start(args, _format);
  886  
  887  			va_copy(copy, args);
  888  			const int length = vsnprintf(nullptr, 0, _format, copy);
  889  			va_end(copy);
  890  
  891  			char* buffer = new char[length + 1];
  892  			va_copy(copy, args);
  893  			vsnprintf(buffer, length + 1, _format, copy);
  894  			va_end(copy);
  895  
  896  			va_end(args);
  897  
  898  			std::string out(buffer);
  899  			delete[] buffer;
  900  
  901  			return out;
  902  
  903  		} // format
  904  
  905  		// Simple XOR scrambling of a string, with an accompanying key
  906  		std::string scramble(const std::string& _input, const std::string& key)
  907  		{
  908  			std::string buffer = _input;
  909  
  910  			for (size_t i = 0; i < _input.size(); ++i) 
  911  			{               
  912  				buffer[i] = _input[i] ^ key[i];
  913  			}
  914  
  915  			return buffer;
  916  
  917  		} // scramble
  918  
  919  		std::vector<std::string> split(const std::string& s, char seperator, bool removeEmptyEntries)
  920  		{			
  921  			std::vector<std::string> output;
  922  
  923  			if (s.empty())
  924  				return output;
  925  			
  926  			const char* src = s.c_str();
  927  
  928  			while (true) 
  929  			{
  930  				const char* d = strchr(src, seperator);
  931  				size_t len = (d) ? d - src : strlen(src);
  932  
  933  				if (len || !removeEmptyEntries)
  934  					output.push_back(std::string(src, len)); // capture token
  935  
  936  				if (d) src += len + 1; else break;
  937  			}
  938  
  939  			return output;
  940  		}
  941  
  942  		std::vector<std::string> splitAny(const std::string& s, const std::string& seperator, bool removeEmptyEntries)
  943  		{
  944  			std::vector<std::string> output;
  945  
  946  			unsigned prev_pos = 0;
  947  			auto pos = s.find_first_of(seperator);
  948  			while (pos != std::string::npos)
  949  			{
  950  				std::string token = s.substr(prev_pos, pos - prev_pos);
  951  				if (!removeEmptyEntries || !token.empty())
  952  					output.push_back(token);
  953  
  954  				pos++;
  955  				prev_pos = pos;
  956  				pos = s.find_first_of(seperator, pos);
  957  			}
  958  
  959  			if (prev_pos < s.length())
  960  			{
  961  				std::string token = s.substr(prev_pos);
  962  				if (!removeEmptyEntries || !token.empty())
  963  					output.push_back(token); // Last word
  964  			}
  965  
  966  			return output;
  967  		}
  968  
  969  		std::string join(const std::vector<std::string>& items, std::string separator)
  970  		{
  971  			std::string data;
  972  
  973  			for (auto line : items)
  974  			{
  975  				if (!data.empty())
  976  					data += separator;
  977  
  978  				data += line;
  979  			}
  980  
  981  			return data;
  982  		}
  983  
  984  		std::string extractString(const std::string& _string, const std::string& startDelimiter, const std::string& endDelimiter, bool keepDelimiter)
  985  		{
  986  			auto ret = extractStrings(_string, startDelimiter, endDelimiter, keepDelimiter);
  987  			if (ret.size() > 0)
  988  				return ret[0];
  989  
  990  			return "";
  991  		}
  992  
  993  		std::vector<std::string> extractStrings(const std::string& _string, const std::string& startDelimiter, const std::string& endDelimiter, bool keepDelimiter)
  994  		{
  995  			std::vector<std::string> ret;
  996  
  997  			if (!startDelimiter.empty() && !endDelimiter.empty())
  998  			{
  999  				size_t pos = 0;
 1000  				while (pos != std::string::npos)
 1001  				{
 1002  					pos = _string.find(startDelimiter, pos);
 1003  					if (pos == std::string::npos)
 1004  						break;
 1005  
 1006  					auto end = _string.find(endDelimiter, pos + startDelimiter.size());
 1007  					if (end == std::string::npos)
 1008  						break;
 1009  
 1010  					std::string value = keepDelimiter ? _string.substr(pos, end - pos + endDelimiter.length()) : _string.substr(pos + startDelimiter.size(), end - (pos + startDelimiter.size()));
 1011  					if (!value.empty())
 1012  						ret.push_back(value);
 1013  
 1014  					pos = end + endDelimiter.size();
 1015  				}
 1016  			}
 1017  
 1018  			return ret;
 1019  		}
 1020  
 1021  		bool startsWithIgnoreCase(const std::string& name1, const std::string& name2)
 1022  		{
 1023  			auto makeUp = [](unsigned int c)
 1024  			{
 1025  				if ((c & 0x80) == 0) return toupper(c);
 1026  				return (int)toupperUnicode(c);
 1027  			};
 1028  
 1029  			size_t p1 = 0;
 1030  			size_t p2 = 0;
 1031  
 1032  			while (true)
 1033  			{
 1034  				int u1 = makeUp(chars2Unicode(name1, p1));
 1035  				int u2 = makeUp(chars2Unicode(name2, p2));
 1036  
 1037  				if (u1 != 0 && u2 == 0)
 1038  					return true;
 1039  				
 1040  				if (u1 != u2)
 1041  					return false;
 1042  			}
 1043  		}
 1044  
 1045  		int compareIgnoreCase(const std::string& name1, const std::string& name2)
 1046  		{
 1047  			size_t p1 = 0;
 1048  			size_t p2 = 0;
 1049  
 1050  			int u1, u2;
 1051  			char c1, c2;
 1052  
 1053  			while (true)
 1054  			{
 1055  				c1 = name1[p1];
 1056  				if ((c1 & 0x80) == 0)
 1057  				{
 1058  					if (c1 >= 'a' && c1 <= 'z')
 1059  						u1 = c1 - 0x20;
 1060  					else
 1061  						u1 = c1;
 1062  
 1063  					p1++;
 1064  				}
 1065  				else 
 1066  					u1 = toupperUnicode(chars2Unicode(name1, p1));
 1067  
 1068  				c2 = name2[p2];
 1069  				if ((c2 & 0x80) == 0)
 1070  				{
 1071  					if (c2 >= 'a' && c2 <= 'z')
 1072  						u2 = c2 - 0x20;
 1073  					else
 1074  						u2 = c2;
 1075  
 1076  					p2++;
 1077  				}
 1078  				else
 1079  					u2 = toupperUnicode(chars2Unicode(name2, p2));
 1080  
 1081  				if (u1 == 0 && u2 != 0)
 1082  					return -1;
 1083  				else if (u1 != 0 && u2 == 0)
 1084  					return 1;
 1085  				else if (u1 == 0 || u2 == 0)
 1086  					return 0;
 1087  
 1088  				u1 -= u2;
 1089  				if (u1)
 1090  					return u1;
 1091  			}
 1092  		}
 1093  
 1094  		bool containsIgnoreCase(const std::string & _string, const std::string & _what)
 1095  		{
 1096  			auto it = std::search(
 1097  				_string.begin(), _string.end(),
 1098  				_what.begin(), _what.end(),
 1099  				[](char ch1, char ch2) { return toupper(ch1) == toupper(ch2); }
 1100  			);
 1101  
 1102  			return (it != _string.end());
 1103  		}
 1104  		
 1105  		bool containsIgnoreCasePinyin(const std::string & _string, const std::string & _what)
 1106  		{
 1107  			std::vector<const char*> vpinyin;
 1108  			size_t len = _string.size();
 1109  			size_t idx = 0;
 1110  			bool ret = false;
 1111  
 1112  			vpinyin.reserve(len);
 1113  			while(idx < len) {
 1114  				int code = chars2Unicode(_string, idx);
 1115  				if (code < 0x80) {
 1116  					vpinyin.push_back( s_tblpinyin[_string[idx-1]] );
 1117  				} else {
 1118  					ret = true;
 1119  					auto it = s_mapPinyin.find(code);
 1120  					if (it != s_mapPinyin.end()) {
 1121  						vpinyin.push_back(it->second);
 1122  					} else {
 1123  						vpinyin.push_back(NULL);
 1124  					}
 1125  				}
 1126  			}
 1127  			if (!ret) return false; // all chars < 0x80
 1128  
 1129  			auto it = std::search(
 1130  				vpinyin.begin(), vpinyin.end(),
 1131  				_what.begin(), _what.end(),
 1132  				[](const char *ptr, char ch2) {
 1133  				    if (!ptr) return false;
 1134  					for(;;) {
 1135  						char ch1 = *ptr++;
 1136  						if (!ch1) return false;
 1137  						if (toupper(ch1) == toupper(ch2)) return true;
 1138  					}
 1139  				}
 1140  			);
 1141  			return (it != vpinyin.end());
 1142  		}
 1143  
 1144  		std::string proper(const std::string& _string)
 1145  		{
 1146  			if (_string.length() <= 1)
 1147  				return Utils::String::toUpper(_string);
 1148  
 1149  			return Utils::String::toUpper(_string.substr(0, 1)) + Utils::String::toLower(_string.substr(1));
 1150  		}
 1151  
 1152  		std::string removeHtmlTags(const std::string& html)
 1153  		{
 1154  			if (html.empty())
 1155  				return html;
 1156  			
 1157  			std::string text = html;
 1158  
 1159  			size_t start = 0, ss = 0;
 1160  			while ((start = text.find("<", (ss = start))) != std::string::npos)
 1161  			{
 1162  				int end = text.find(">", start);
 1163  				if (end != std::string::npos && end >= start)
 1164  					text = text.erase(start, end - start + 1);
 1165  				else
 1166  				{
 1167  					start++;
 1168  					if (start >= text.size())
 1169  						break;
 1170  				}
 1171  			}
 1172  			
 1173  			return trim(text);
 1174  		}
 1175  
 1176  		unsigned int fromHexString(const std::string& string)
 1177  		{
 1178  			if (string.empty())
 1179  				return 0;
 1180  
 1181  			unsigned int value = 0;
 1182  
 1183  			int dec = 0;
 1184  			for (int i = string.length() - 1; i >= 0; i--)
 1185  			{
 1186  				char c = string[i];
 1187  				if (c == ' ')
 1188  					continue;
 1189  
 1190  				if (c == 'x' || c == 'X')
 1191  					return value;
 1192  
 1193  				if (c >= '0' && c <= '9')
 1194  					value += (c - '0') << dec;
 1195  				else if (c >= 'A' && c <= 'F')
 1196  					value += (c - 'A' + 10) << dec;
 1197  				else if (c >= 'a' && c <= 'f')
 1198  					value += (c - 'a' + 10) << dec;
 1199  				else
 1200  					return 0;
 1201  
 1202  				dec += 4;
 1203  			}
 1204  
 1205  			return value;
 1206  		}
 1207  
 1208  		int	toInteger(const std::string& string)
 1209  		{
 1210  			if (string.empty())
 1211  				return 0;
 1212  
 1213  			const char* str = string.c_str();
 1214  			while (*str == ' ')
 1215  				str++;
 1216  
 1217  			bool neg = false;
 1218  			if (*str == '-')
 1219  			{
 1220  				neg = true;
 1221  				++str;
 1222  			}
 1223  			else if (*str == '+')
 1224  				++str;
 1225  
 1226  			int64_t value = 0;
 1227  			for (; *str && *str != '.' && *str != ' ' && *str != '\r' && *str != '\n'; str++)
 1228  			{
 1229  				if (*str < '0' || *str > '9')
 1230  					return 0;
 1231  
 1232  				value *= 10;
 1233  				value += *str - '0';
 1234  			}
 1235  
 1236  			return neg ? -value : value;
 1237  		}
 1238  
 1239  		bool toBoolean(const std::string& string)
 1240  		{
 1241  			// only look at first char
 1242  			char first = string[0];
 1243  
 1244  			// 1*, t* (true), T* (True), y* (yes), Y* (YES)
 1245  			return (first == '1' || first == 't' || first == 'T' || first == 'y' || first == 'Y');
 1246  		}
 1247  
 1248  		float toFloat(const std::string& string)
 1249  		{
 1250  			if (string.empty())
 1251  				return 0.0f;
 1252  
 1253  			const char* str = string.c_str();
 1254  			while (*str == ' ')
 1255  				str++;
 1256  
 1257  			bool neg = false;
 1258  			if (*str == '-') 
 1259  			{
 1260  				neg = true;
 1261  				++str;
 1262  			}
 1263  			else if (*str == '+')
 1264  				++str;
 1265  			
 1266  			int64_t value = 0;
 1267  			for (; *str && *str != '.' && *str != ' '; str++)
 1268  			{
 1269  				if (*str < '0' || *str > '9')
 1270  					return 0;
 1271  
 1272  				value *= 10;
 1273  				value += *str - '0';
 1274  			}
 1275  
 1276  			if (*str == '.')
 1277  			{
 1278  				str++;
 1279  
 1280  				int64_t decimal = 0, weight = 1;
 1281  
 1282  				for (; *str && *str != ' '; str++)
 1283  				{
 1284  					if (*str < '0' || *str > '9')
 1285  						return 0;
 1286  
 1287  					decimal *= 10;
 1288  					decimal += *str - '0';
 1289  					weight *= 10;
 1290  				}
 1291  
 1292  				float ret = value + (decimal / (float)weight);
 1293  				return neg ? -ret : ret;
 1294  			}
 1295  
 1296  			return neg ? -value : value;
 1297  		}
 1298  
 1299  		double toDouble(const std::string& string)
 1300  		{
 1301  			if (string.empty())
 1302  				return 0.0f;
 1303  
 1304  			const char* str = string.c_str();
 1305  			while (*str == ' ')
 1306  				str++;
 1307  
 1308  			bool neg = false;
 1309  			if (*str == '-')
 1310  			{
 1311  				neg = true;
 1312  				++str;
 1313  			}
 1314  			else if (*str == '+')
 1315  				++str;
 1316  
 1317  			int64_t value = 0;
 1318  			for (; *str && *str != '.' && *str != ' '; str++)
 1319  			{
 1320  				if (*str < '0' || *str > '9')
 1321  					return 0;
 1322  
 1323  				value *= 10;
 1324  				value += *str - '0';
 1325  			}
 1326  
 1327  			if (*str == '.')
 1328  			{
 1329  				str++;
 1330  
 1331  				int64_t decimal = 0, weight = 1;
 1332  
 1333  				for (; *str && *str != ' '; str++)
 1334  				{
 1335  					if (*str < '0' || *str > '9')
 1336  						return 0;
 1337  
 1338  					decimal *= 10;
 1339  					decimal += *str - '0';
 1340  					weight *= 10;
 1341  				}
 1342  
 1343  				double ret = value + (decimal / (double)weight);
 1344  				return neg ? -ret : ret;
 1345  			}
 1346  
 1347  			return neg ? -value : value;
 1348  		}
 1349  
 1350  		std::string decodeXmlString(const std::string& string)
 1351  		{
 1352  			std::string ret = string;
 1353  
 1354  			ret = replace(ret, "&amp;", "&");
 1355  			ret = replace(ret, "&apos;", "'");
 1356  			ret = replace(ret, "&lt;", "<");
 1357  			ret = replace(ret, "&gt;", ">");
 1358  			ret = replace(ret, "&quot;", "\"");
 1359  			ret = replace(ret, "&nbsp;", " ");
 1360  			ret = replace(ret, "&#39;", "'");
 1361  
 1362  			return ret;
 1363  		}
 1364  
 1365  		std::string toHexString(unsigned int color)
 1366  		{
 1367  			char hex[10];
 1368  			hex[0] = 0;
 1369  			auto len = snprintf(hex, sizeof(hex) - 1, "%08X", color);
 1370  			hex[len] = 0;
 1371  			return hex;
 1372  		}
 1373  
 1374  		std::string padLeft(const std::string& data, const size_t& totalWidth, const char& padding)
 1375  		{
 1376  			if (data.length() >= totalWidth)
 1377  				return data;
 1378  
 1379  			std::string ret = data;
 1380  			ret.insert(0, totalWidth - ret.length(), padding);
 1381  			return ret;
 1382  		}
 1383  
 1384  		int occurs(const std::string& str, char target)
 1385  		{
 1386  			int count = 0;
 1387  			
 1388  			for (char ch : str)
 1389  				if (ch == target)
 1390  					count++;
 1391  
 1392  			return count;
 1393  		}
 1394  
 1395  		bool isPrintableChar(char c)
 1396  		{			
 1397  #if defined(_WIN32)
 1398  			return isprint(c);
 1399  #else
 1400  			return std::isprint(c);
 1401  #endif
 1402  		}
 1403  
 1404  		bool isKorean(const unsigned int uni)
 1405  		{
 1406  			return (uni >= 0x3131 && uni <= 0x3163) ||  // Unicode range for Hangul consonants and vowels (ㄱ to ㅣ)
 1407  				(uni >= 0xAC00 && uni <= 0xD7A3);       // Unicode range for Hangul syllables (가 to 힣)
 1408  		}
 1409  
 1410  		bool isKorean(const char* _string, bool checkFirstChar)
 1411  		{
 1412  			if (!_string)
 1413  				return false;
 1414  
 1415  			size_t len = strlen(_string);
 1416  			if (len < 3)
 1417  				return false;
 1418  
 1419  			const char* target = _string;
 1420  			if (!checkFirstChar)
 1421  			{
 1422  				const char* ptr = _string + len - 1;
 1423  				while (ptr > _string && (*ptr & 0xC0) == 0x80)
 1424  					ptr--;
 1425  
 1426  				target = ptr;
 1427  			}
 1428  
 1429  			size_t cursor = 0;
 1430  			unsigned int uni = chars2Unicode(std::string(target, 3), cursor);
 1431  
 1432  			return isKorean(uni);
 1433  		} // isKorean
 1434  
 1435  		KoreanCharType getKoreanCharType(const char* _string)
 1436  		{
 1437  			if (!_string || strlen(_string) != 3)
 1438  				return KoreanCharType::NONE;
 1439  
 1440  			size_t cursor = 0;
 1441  			unsigned int uni = chars2Unicode(std::string(_string), cursor);
 1442  
 1443  			if (uni >= 0x3131 && uni <= 0x314E)
 1444  				return KoreanCharType::JAEUM;
 1445  
 1446  			if (uni >= 0x314F && uni <= 0x3163)
 1447  				return KoreanCharType::MOEUM;
 1448  
 1449  			return KoreanCharType::NONE;
 1450  
 1451  		} // getKoreanCharType
 1452  
 1453  		bool splitHangulSyllable(const char* input, const char** chosung, const char** joongsung, const char** jongsung)
 1454  		{
 1455  			if (!input)
 1456  				return false;
 1457  
 1458  			size_t len = strlen(input);
 1459  			if (len < 3)
 1460  				return false;
 1461  
 1462  			switch (getKoreanCharType(input))
 1463  			{
 1464  			case KoreanCharType::JAEUM:
 1465  				*chosung = input;
 1466  				break;
 1467  			case KoreanCharType::MOEUM:
 1468  				if (joongsung) *joongsung = input;
 1469  				break;
 1470  			default:
 1471  				size_t cursor = 0;
 1472  				unsigned int unicode = chars2Unicode(input, cursor) - 0xAC00;
 1473  
 1474  				int chosungIdx = unicode / (28 * 21);
 1475  				int joongsungIdx = (unicode / 28) % 21;
 1476  				int jongsungIdx = unicode % 28;
 1477  
 1478  				*chosung = KOREAN_CHOSUNG_LIST.at(chosungIdx);
 1479  				if (joongsung) *joongsung = KOREAN_JOONGSUNG_LIST.at(joongsungIdx);
 1480  				if (jongsung) *jongsung = KOREAN_JONGSUNG_LIST.at(jongsungIdx);
 1481  				break;
 1482  			}
 1483  
 1484  			return true;
 1485  		}
 1486  
 1487  		void koreanTextInput(const char* text, std::string& componentText, unsigned int& componentCursor)
 1488  		{
 1489  			if (!text)
 1490  				return;
 1491  
 1492  			if (strlen(text) != 3)
 1493  				return;
 1494  
 1495  			if (componentText.size() < 3)
 1496  				return;
 1497  
 1498  			KoreanCharType charType = getKoreanCharType(text);
 1499  
 1500  			std::string lastCharString = componentText.substr(componentCursor - 3, 3);
 1501  			const char* lastChar = lastCharString.c_str();
 1502  
 1503  			const char* chosung = "";
 1504  			const char* joongsung = "";
 1505  			const char* jongsung = "";
 1506  			splitHangulSyllable(lastChar, &chosung, &joongsung, &jongsung);
 1507  
 1508  			auto eraseAndInsert = [&](const std::string& toInsert, bool moveCursorLeft = true)
 1509  			{
 1510  				size_t cursor = prevCursor(componentText, componentCursor);
 1511  				componentText.erase(componentText.begin() + cursor, componentText.begin() + componentCursor);
 1512  				componentText.insert(cursor, toInsert);
 1513  				if (moveCursorLeft)
 1514  					componentCursor -= 3;
 1515  			};
 1516  
 1517  			auto makeHangul = [&](int chosungIdx, int joongsungIdx, int jongsungIdx) -> std::string
 1518  			{
 1519  				unsigned int code = ((chosungIdx * 21) + joongsungIdx) * 28 + jongsungIdx + 0xAC00;
 1520  				return unicode2Chars(code);
 1521  			};
 1522  
 1523  			auto findIndex = [&](const std::vector<const char*>& vec, const char* key) -> int 
 1524  			{
 1525  				auto it = std::find_if(vec.begin(), vec.end(), [&](const char* item)
 1526  				{
 1527  					return std::strcmp(item, key) == 0;
 1528  				});
 1529  
 1530  				return (it != vec.end()) ? std::distance(vec.begin(), it) : -1;
 1531  			};
 1532  
 1533  			if (!strcmp(lastChar, chosung) && charType == KoreanCharType::JAEUM)
 1534  			{
 1535  				std::string combine = std::string(chosung) + text;
 1536  
 1537  				int idx = findIndex(KOREAN_GYEOP_BATCHIM_COMBINATIONS, combine.c_str());
 1538  				if (idx != -1)
 1539  					eraseAndInsert(KOREAN_GYEOP_BATCHIM_LIST.at(idx));
 1540  				else
 1541  					componentText.insert(componentCursor, text);
 1542  			}
 1543  			else if (!strcmp(lastChar, chosung) && charType == KoreanCharType::MOEUM)
 1544  			{
 1545  				int joongsungIdx = findIndex(KOREAN_JOONGSUNG_LIST, text);
 1546  
 1547  				int gyeopBatchimIdx = findIndex(KOREAN_GYEOP_BATCHIM_LIST, lastChar);
 1548  				if (gyeopBatchimIdx != -1)
 1549  				{
 1550  					char jaeum1[4] = {};
 1551  					strncpy(jaeum1, KOREAN_GYEOP_BATCHIM_COMBINATIONS.at(gyeopBatchimIdx), 3);
 1552  					jaeum1[3] = '\0';
 1553  
 1554  					char jaeum2[4] = {};
 1555  					strncpy(jaeum2, KOREAN_GYEOP_BATCHIM_COMBINATIONS.at(gyeopBatchimIdx) + 3, 3);
 1556  					jaeum2[3] = '\0';
 1557  
 1558  					int chosungIdx = findIndex(KOREAN_CHOSUNG_LIST, static_cast<const char*>(jaeum2));
 1559  					std::string hangul = std::string(jaeum1) + makeHangul(chosungIdx, joongsungIdx, 0);
 1560  
 1561  					eraseAndInsert(hangul, false);
 1562  				}
 1563  				else
 1564  				{
 1565  					int chosungIdx = findIndex(KOREAN_CHOSUNG_LIST, lastChar);
 1566  					std::string hangul = makeHangul(chosungIdx, joongsungIdx, 0);
 1567  
 1568  					eraseAndInsert(hangul);
 1569  				}
 1570  			}
 1571  			else if (!strcmp(lastChar, joongsung) && charType == KoreanCharType::JAEUM)
 1572  			{
 1573  				componentText.insert(componentCursor, text);
 1574  			}
 1575  			else if (!strcmp(lastChar, joongsung) && charType == KoreanCharType::MOEUM)
 1576  			{
 1577  				std::string combine = std::string(lastChar) + text;
 1578  
 1579  				int idx = findIndex(KOREAN_IJUNG_MOEUM_COMBINATIONS, combine.c_str());
 1580  				if (idx != -1)
 1581  					eraseAndInsert(KOREAN_IJUNG_MOEUM_LIST.at(idx));
 1582  				else
 1583  					componentText.insert(componentCursor, text);
 1584  			}
 1585  			else if (strcmp(jongsung, " ") && charType == KoreanCharType::JAEUM)
 1586  			{
 1587  				std::string combine = std::string(jongsung) + text;
 1588  
 1589  				int idx = findIndex(KOREAN_GYEOP_BATCHIM_COMBINATIONS, combine.c_str());
 1590  
 1591  				if (idx != -1)
 1592  				{
 1593  					int chosungIdx = findIndex(KOREAN_CHOSUNG_LIST, chosung);
 1594  					int joongsungIdx = findIndex(KOREAN_JOONGSUNG_LIST, joongsung);
 1595  					int jongsungIdx = findIndex(KOREAN_JONGSUNG_LIST, KOREAN_GYEOP_BATCHIM_LIST.at(idx));
 1596  					std::string hangul = makeHangul(chosungIdx, joongsungIdx, jongsungIdx);
 1597  
 1598  					eraseAndInsert(hangul);
 1599  				}
 1600  				else
 1601  				{
 1602  					componentText.insert(componentCursor, text);
 1603  				}
 1604  			}
 1605  			else if (strcmp(jongsung, " ") && charType == KoreanCharType::MOEUM)
 1606  			{
 1607  				int idx = findIndex(KOREAN_GYEOP_BATCHIM_LIST, jongsung);
 1608  				if (idx != -1)
 1609  				{
 1610  					char jaeum1[4] = {};
 1611  					strncpy(jaeum1, KOREAN_GYEOP_BATCHIM_COMBINATIONS.at(idx), 3);
 1612  					jaeum1[3] = '\0';
 1613  
 1614  					char jaeum2[4] = {};
 1615  					strncpy(jaeum2, KOREAN_GYEOP_BATCHIM_COMBINATIONS.at(idx) + 3, 3);
 1616  					jaeum2[3] = '\0';
 1617  
 1618  					int chosungIdx = findIndex(KOREAN_CHOSUNG_LIST, chosung);
 1619  					int joongsungIdx = findIndex(KOREAN_JOONGSUNG_LIST, joongsung);
 1620  					int jongsungIdx = findIndex(KOREAN_JONGSUNG_LIST, static_cast<const char*>(jaeum1));
 1621  					std::string hangul = makeHangul(chosungIdx, joongsungIdx, jongsungIdx);
 1622  
 1623  					chosungIdx = findIndex(KOREAN_CHOSUNG_LIST, static_cast<const char*>(jaeum2));
 1624  					joongsungIdx = findIndex(KOREAN_JOONGSUNG_LIST, text);
 1625  					hangul += makeHangul(chosungIdx, joongsungIdx, 0);
 1626  
 1627  					eraseAndInsert(hangul, false);
 1628  				}
 1629  				else
 1630  				{
 1631  					int chosungIdx = findIndex(KOREAN_CHOSUNG_LIST, chosung);
 1632  					int joongsungIdx = findIndex(KOREAN_JOONGSUNG_LIST, joongsung);
 1633  					std::string hangul = makeHangul(chosungIdx, joongsungIdx, 0);
 1634  
 1635  					chosungIdx = findIndex(KOREAN_CHOSUNG_LIST, jongsung);
 1636  					joongsungIdx = findIndex(KOREAN_JOONGSUNG_LIST, text);
 1637  					hangul += makeHangul(chosungIdx, joongsungIdx, 0);
 1638  
 1639  					eraseAndInsert(hangul, false);
 1640  				}
 1641  			}
 1642  			else if (!strcmp(jongsung, " ") && charType == KoreanCharType::JAEUM)
 1643  			{
 1644  				int jongsungIdx = findIndex(KOREAN_JONGSUNG_LIST, text);
 1645  
 1646  				if (jongsungIdx != -1)
 1647  				{
 1648  					int chosungIdx = findIndex(KOREAN_CHOSUNG_LIST, chosung);
 1649  					int joongsungIdx = findIndex(KOREAN_JOONGSUNG_LIST, joongsung);
 1650  					std::string hangul = makeHangul(chosungIdx, joongsungIdx, jongsungIdx);
 1651  
 1652  					eraseAndInsert(hangul);
 1653  				}
 1654  				else
 1655  				{
 1656  					componentText.insert(componentCursor, text);
 1657  				}
 1658  			}
 1659  			else if (!strcmp(jongsung, " ") && charType == KoreanCharType::MOEUM)
 1660  			{
 1661  				std::string combine = std::string(joongsung) + text;
 1662  
 1663  				int idx = findIndex(KOREAN_IJUNG_MOEUM_COMBINATIONS, combine.c_str());
 1664  				if (idx != -1)
 1665  				{
 1666  					int chosungIdx = findIndex(KOREAN_CHOSUNG_LIST, chosung);
 1667  					int joongsungIdx = findIndex(KOREAN_JOONGSUNG_LIST, KOREAN_IJUNG_MOEUM_LIST.at(idx));
 1668  					std::string hangul = makeHangul(chosungIdx, joongsungIdx, 0);
 1669  
 1670  					eraseAndInsert(hangul);
 1671  				}
 1672  				else
 1673  				{
 1674  					componentText.insert(componentCursor, text);
 1675  				}
 1676  			}
 1677  
 1678  			size_t newCursor = nextCursor(componentText, componentCursor);
 1679  			componentCursor = (unsigned int)newCursor;
 1680  		}
 1681  		// koreanTextInput
 1682  
 1683  #if defined(_WIN32)
 1684  		const std::string convertFromWideString(const std::wstring& wstring)
 1685  		{
 1686  			int numBytes = WideCharToMultiByte(CP_UTF8, 0, wstring.c_str(), (int)wstring.length(), nullptr, 0, nullptr, nullptr);
 1687  			
 1688  			std::string string(numBytes, 0);			
 1689  			WideCharToMultiByte(CP_UTF8, 0, wstring.c_str(), (int)wstring.length(), (char*)string.c_str(), numBytes, nullptr, nullptr);
 1690  
 1691  			return string;
 1692  		}
 1693  
 1694  		const std::wstring convertToWideString(const std::string& string)
 1695  		{
 1696  			int numBytes = MultiByteToWideChar(CP_UTF8, 0, string.c_str(), (int)string.length(), nullptr, 0);
 1697  
 1698  			std::wstring wstring(numBytes, 0);			
 1699  			MultiByteToWideChar(CP_UTF8, 0, string.c_str(), (int)string.length(), (WCHAR*)wstring.c_str(), numBytes);
 1700  
 1701  			return wstring;
 1702  		}
 1703  #endif
 1704  	} // String::
 1705  
 1706  } // Utils::
```

## src/utils/StringUtil.h (whole, fork-modified, at the pin)

```text
    1  #pragma once
    2  #ifndef ES_CORE_UTILS_STRING_UTIL_H
    3  #define ES_CORE_UTILS_STRING_UTIL_H
    4  
    5  #include <string>
    6  #include <cstring>
    7  #include <vector>
    8  
    9  namespace Utils
   10  {
   11  	namespace String
   12  	{
   13  		typedef std::vector<std::string> stringVector;
   14  
   15  		unsigned int chars2Unicode      (const std::string& _string, size_t& _cursor);
   16  		std::string  unicode2Chars      (const unsigned int _unicode);
   17  		size_t       nextCursor         (const std::string& _string, const size_t _cursor);
   18  		size_t       prevCursor         (const std::string& _string, const size_t _cursor);
   19  		size_t       moveCursor         (const std::string& _string, const size_t _cursor, const int _amount);
   20  		std::string  toLower            (const std::string& _string);
   21  		std::string  toUpper            (const std::string& _string);
   22  		std::string  trim               (const std::string& _string);
   23  		std::string  shellQuote         (const std::string& _string);
   24  		std::string  maskSecrets        (const std::string& _string); // a command line, URL or query with every credential value <redacted> (fork #177)
   25  		std::string  replace            (const std::string& _string, const std::string& _replace, const std::string& _with);
   26  		bool         startsWith         (const std::string& _string, const std::string& _start);
   27  		bool         endsWith           (const std::string& _string, const std::string& _end);
   28  		std::string  removeParenthesis  (const std::string& _string);		
   29  		std::string  vectorToCommaString(stringVector _vector);
   30  		stringVector commaStringToVector(const std::string& _string);
   31  		std::string  format             (const char* _string, ...);
   32  		std::string  scramble           (const std::string& _input, const std::string& key);
   33  
   34  		std::vector<std::string> split  (const std::string& s, char seperator, bool removeEmptyEntries = false);
   35  		std::vector<std::string> splitAny(const std::string& s, const std::string& seperator, bool removeEmptyEntries = false);
   36  		std::vector<std::string> extractStrings(const std::string& _string, const std::string& startDelimiter, const std::string& endDelimiter, bool keepDelimiter = false);
   37  		std::string              extractString(const std::string& _string, const std::string& startDelimiter, const std::string& endDelimiter, bool keepDelimiter = false);
   38  
   39  		std::string join(const std::vector<std::string>& items, std::string separator);
   40  		int			compareIgnoreCase(const std::string& name1, const std::string& name2);
   41  		std::string proper(const std::string& _string);
   42  		std::string removeHtmlTags(const std::string& html);
   43  		bool        containsIgnoreCase(const std::string & _string, const std::string & _what);
   44  		bool        containsIgnoreCasePinyin(const std::string & _string, const std::string & _what);
   45  		bool		startsWithIgnoreCase(const std::string& name1, const std::string& name2);
   46  
   47  		int			toInteger(const std::string& string);
   48  		float		toFloat(const std::string& string);
   49  		double		toDouble(const std::string& string);
   50  		bool		toBoolean(const std::string& string);
   51  
   52  		std::string decodeXmlString(const std::string& string);
   53  		std::string toHexString(unsigned int color);
   54  		unsigned int fromHexString(const std::string& string);
   55  
   56  		std::string padLeft(const std::string& data, const size_t& totalWidth, const char& padding);
   57  
   58  		int			occurs(const std::string& str, char target);
   59  		bool		isPrintableChar(char c);
   60  
   61  		// for Korean text input
   62  		const std::vector<const char*> KOREAN_CHOSUNG_LIST = { "ㄱ", "ㄲ", "ㄴ", "ㄷ", "ㄸ", "ㄹ", "ㅁ", "ㅂ", "ㅃ", "ㅅ", "ㅆ", "ㅇ", "ㅈ", "ㅉ", "ㅊ", "ㅋ", "ㅌ", "ㅍ", "ㅎ" };
   63  		const std::vector<const char*> KOREAN_JOONGSUNG_LIST = { "ㅏ", "ㅐ", "ㅑ", "ㅒ", "ㅓ", "ㅔ", "ㅕ", "ㅖ", "ㅗ", "ㅘ", "ㅙ", "ㅚ", "ㅛ", "ㅜ", "ㅝ", "ㅞ", "ㅟ", "ㅠ", "ㅡ", "ㅢ", "ㅣ" };
   64  		const std::vector<const char*> KOREAN_JONGSUNG_LIST = { " ", "ㄱ", "ㄲ", "ㄳ", "ㄴ", "ㄵ", "ㄶ", "ㄷ", "ㄹ", "ㄺ", "ㄻ", "ㄼ", "ㄽ", "ㄾ", "ㄿ", "ㅀ", "ㅁ", "ㅂ", "ㅄ", "ㅅ", "ㅆ", "ㅇ", "ㅈ", "ㅊ", "ㅋ", "ㅌ", "ㅍ", "ㅎ" };
   65  		const std::vector<const char*> KOREAN_GYEOP_BATCHIM_LIST = { "ㄳ", "ㄵ", "ㄶ", "ㄺ", "ㄻ", "ㄼ", "ㄽ", "ㄾ", "ㄿ", "ㅀ", "ㅄ" };
   66  		const std::vector<const char*> KOREAN_GYEOP_BATCHIM_COMBINATIONS = { "ㄱㅅ", "ㄴㅈ", "ㄴㅎ", "ㄹㄱ", "ㄹㅁ", "ㄹㅂ", "ㄹㅅ", "ㄹㅌ", "ㄹㅍ", "ㄹㅎ", "ㅂㅅ" };
   67  		const std::vector<const char*> KOREAN_IJUNG_MOEUM_LIST = { "ㅘ", "ㅙ", "ㅚ", "ㅝ", "ㅞ", "ㅟ", "ㅢ" };
   68  		const std::vector<const char*> KOREAN_IJUNG_MOEUM_COMBINATIONS = { "ㅗㅏ", "ㅗㅐ", "ㅗㅣ", "ㅜㅓ", "ㅜㅔ", "ㅜㅣ", "ㅡㅣ" };
   69  		enum KoreanCharType : unsigned int
   70  		{
   71  			NONE = 0,
   72  			JAEUM = 1,
   73  			MOEUM = 2,
   74  		};
   75  		bool			isKorean(const unsigned int uni);
   76  		bool			isKorean(const char* _string, bool checkFirstChar = true);
   77  		KoreanCharType	getKoreanCharType(const char* _string);
   78  		bool			splitHangulSyllable(const char* input, const char** chosung, const char** joongsung = nullptr, const char** jongsung = nullptr);
   79  		void			koreanTextInput(const char* text, std::string& componentText, unsigned int& componentCursor);
   80  		// end Korean text input
   81  
   82  #if defined(_WIN32)
   83  		const std::string convertFromWideString(const std::wstring& wstring);
   84  		const std::wstring convertToWideString(const std::string& string);
   85  #endif
   86  	} // String::
   87  
   88  } // Utils::
   89  
   90  #if defined(_WIN32)
   91  #define WINSTRINGW(x) Utils::String::convertToWideString(x)
   92  #else
   93  #define WINSTRINGW(x) x
   94  #endif
   95  
   96  #endif // ES_CORE_UTILS_STRING_UTIL_H
```

## src/utils/ThreadPool.cpp `:18-34` (an excerpt, upstream-carried, at the pin)

```text
   18  		mPoolName = poolName;
   19  		mThreadByCore = threadByCore;
   20  	}
   21  
   22  	void ThreadPool::start()
   23  	{
   24  		mRunning = true;
   25  
   26  		size_t num_threads = mThreadByCore < 0 ? abs(mThreadByCore) : std::thread::hardware_concurrency() * mThreadByCore;
   27  
   28  		auto doWork = [&](size_t id)
   29  		{
   30  #if WIN32
   31  			if (Utils::Platform::isWindows10())
   32  			{
   33  				if (!mPoolName.empty())
   34  				{
```

## src/utils/ThreadPool.cpp `:76-99` (an excerpt, upstream-carried, at the pin)

```text
   76  					std::this_thread::sleep_for(std::chrono::milliseconds(1));
   77  				}
   78  			}
   79  		};
   80  
   81  		mThreads.reserve(num_threads);
   82  
   83  		for (size_t i = 0; i < num_threads; i++)
   84  			mThreads.push_back(std::thread(doWork, i));
   85  	}
   86  
   87  	ThreadPool::~ThreadPool()
   88  	{
   89  		mRunning = false;
   90  
   91  		for (std::thread& t : mThreads)
   92  			if (t.joinable())
   93  				t.join();
   94  	}
   95  
   96  	WorkItemPtr  ThreadPool::queueWorkItem(work_function work)
   97  	{
   98  		auto item = std::make_shared<WorkItem>();
   99  
```

## src/utils/TimeText.cpp (whole, fork-added, at the pin)

```text
    1  #include "utils/TimeText.h"
    2  
    3  #include <stdio.h>
    4  
    5  namespace Utils
    6  {
    7  	namespace Time
    8  	{
    9  		std::string clockText(const tm& t, bool twelveHour, const std::string& localeMarker)
   10  		{
   11  			char buf[16];
   12  
   13  			if (!twelveHour)
   14  			{
   15  				snprintf(buf, sizeof(buf), "%02d:%02d", t.tm_hour, t.tm_min);
   16  				return buf;
   17  			}
   18  
   19  			// %I: 1 to 12, with midnight and noon both written 12.
   20  			int hour = t.tm_hour % 12;
   21  			if (hour == 0)
   22  				hour = 12;
   23  			snprintf(buf, sizeof(buf), "%02d:%02d", hour, t.tm_min);
   24  
   25  			const std::string marker = !localeMarker.empty() ? localeMarker : (t.tm_hour < 12 ? "AM" : "PM");
   26  			return std::string(buf) + " " + marker;
   27  		}
   28  
   29  		// Days since 1970-01-01 for a civil date, so two tm values compare
   30  		// as calendar days without any year-length or leap arithmetic here
   31  		// (Howard Hinnant's days_from_civil; valid for every year the tm
   32  		// can hold).
   33  		static long dayNumber(const tm& t)
   34  		{
   35  			long y = t.tm_year + 1900;
   36  			const unsigned m = (unsigned)(t.tm_mon + 1);
   37  			const unsigned d = (unsigned)t.tm_mday;
   38  			y -= m <= 2;
   39  			const long era = (y >= 0 ? y : y - 399) / 400;
   40  			const unsigned yoe = (unsigned)(y - era * 400);
   41  			const unsigned doy = (153 * (m + (m > 2 ? -3 : 9)) + 2) / 5 + d - 1;
   42  			const unsigned doe = yoe * 365 + yoe / 4 - yoe / 100 + doy;
   43  			return era * 146097 + (long)doe - 719468;
   44  		}
   45  
   46  		DayRelation dayRelation(const tm& stamp, const tm& now)
   47  		{
   48  			const long ago = dayNumber(now) - dayNumber(stamp);
   49  			if (ago == 0)
   50  				return DayRelation::Today;
   51  			if (ago == 1)
   52  				return DayRelation::Yesterday;
   53  			return DayRelation::Older;
   54  		}
   55  
   56  		std::string shortYear(const std::string& localeDate)
   57  		{
   58  			// The first run of exactly four digits bounded by non-digits is
   59  			// the year in every locale's %x that writes one; keep its last two.
   60  			for (size_t i = 0; i + 4 <= localeDate.size(); i++)
   61  			{
   62  				bool run = true;
   63  				for (size_t k = 0; k < 4; k++)
   64  					if (!isdigit((unsigned char)localeDate[i + k])) { run = false; break; }
   65  				if (!run)
   66  					continue;
   67  				const bool before = (i == 0) || !isdigit((unsigned char)localeDate[i - 1]);
   68  				const bool after = (i + 4 == localeDate.size()) || !isdigit((unsigned char)localeDate[i + 4]);
   69  				if (before && after)
   70  					return localeDate.substr(0, i) + localeDate.substr(i + 2);
   71  			}
   72  			return localeDate;
   73  		}
   74  
   75  		std::string whenText(DayRelation relation, const std::string& shortDate, const std::string& timeText,
   76  		                     const std::string& todayWord, const std::string& yesterdayWord, const std::string& atWord)
   77  		{
   78  			const std::string day = (relation == DayRelation::Today) ? todayWord
   79  			                      : (relation == DayRelation::Yesterday) ? yesterdayWord : shortDate;
   80  			return day + " " + atWord + " " + timeText;
   81  		}
   82  	}
   83  }
```

## src/utils/TimeText.h (whole, fork-added, at the pin)

```text
    1  #pragma once
    2  #ifndef ES_CORE_UTILS_TIME_TEXT_H
    3  #define ES_CORE_UTILS_TIME_TEXT_H
    4  
    5  #include <string>
    6  #include <time.h>
    7  
    8  // The time of day as the player reads it beside a date (fork #195, D-UI-058).
    9  //
   10  // Pure: a tm and what the caller already knows -- the switch, and what the
   11  // locale says for %p -- so es-app/tests/unit can hold it to its word. The
   12  // shell that asks Settings and strftime is DateTime::toLocalTimeString in
   13  // TimeUtil.cpp; the SAVE STATE MANAGER's tiles are what this was written for.
   14  namespace Utils
   15  {
   16  	namespace Time
   17  	{
   18  		// t:            as localtime fills it; tm_hour 0..23, tm_min 0..59.
   19  		// twelveHour:   SHOW CLOCK IN 12-HOUR FORMAT, read at the call.
   20  		// localeMarker: the locale's %p for this hour -- "AM"/"PM" in English,
   21  		//               empty in French and most of Europe. On the 12-hour
   22  		//               clock an empty marker gets a literal AM or PM from the
   23  		//               hour instead, because "09:07" alone is exactly what
   24  		//               the switch was turned on to avoid.
   25  		// Off the switch: HH:MM, as %R prints it, marker or no marker.
   26  		// On it: hh:MM and the marker, as %I:%M %p prints it -- the clock in
   27  		// the corner and the cloud rows' LAST lines use the same form.
   28  		std::string clockText(const tm& t, bool twelveHour, const std::string& localeMarker);
   29  
   30  		// Which day a stamp falls on, as a player would say it (fork #195,
   31  		// D-UI-087): TODAY reads as the time alone, YESTERDAY as that word
   32  		// and the time, OLDER as the date and the time. Calendar days in
   33  		// local time, so 23:59 and 00:01 across midnight are a day apart
   34  		// and December 31st to January 1st is one day too. A stamp on a
   35  		// later day than now is OLDER: the date is the honest thing to show
   36  		// for a clock that was wrong when the file was written.
   37  		enum class DayRelation { Today, Yesterday, Older };
   38  		DayRelation dayRelation(const tm& stamp, const tm& now);
   39  
   40  		// The locale's date with a two-digit year: "09/24/2026" -> "09/24/26",
   41  		// "24/09/2026" -> "24/09/26". A save is not from another century, and
   42  		// the two characters buy the word between the date and the time
   43  		// (fork #195, D-UI-089, the maintainer's call). A date with no
   44  		// four-digit year is returned as it came.
   45  		std::string shortYear(const std::string& localeDate);
   46  
   47  		// When a save was made, as the tile says it (D-UI-089): "TODAY at
   48  		// 17:07", "YESTERDAY at 14:03", "09/24/26 at 14:03". The words come
   49  		// translated from the caller -- TODAY, YESTERDAY in the label case,
   50  		// "at" lower-case by the maintainer's word ("adding 'at', in
   51  		// lowercase, if possible"), the a-grave in French.
   52  		std::string whenText(DayRelation relation, const std::string& shortDate, const std::string& timeText,
   53  		                     const std::string& todayWord, const std::string& yesterdayWord, const std::string& atWord);
   54  	}
   55  }
   56  
   57  #endif // ES_CORE_UTILS_TIME_TEXT_H
```

## src/utils/TimeUtil.cpp (whole, fork-modified, at the pin)

```text
    1  #include "utils/TimeUtil.h"
    2  #include "utils/TimeText.h"
    3  #include "utils/StringUtil.h"
    4  #include "LocaleES.h"
    5  #include "Settings.h"
    6  
    7  #if WIN32
    8  #include <Windows.h>
    9  #elif defined(__linux__)
   10  #include <langinfo.h>
   11  #endif
   12  
   13  namespace Utils
   14  {
   15  	namespace Time
   16  	{
   17  		std::string getSystemDateFormat(bool includeHours)
   18  		{
   19  			static std::string value;
   20  			if (!includeHours && !value.empty())
   21  				return value;
   22  
   23  			static std::string valueWithHours;
   24  			if (includeHours && !valueWithHours.empty())
   25  				return valueWithHours;
   26  
   27  			std::string ret;
   28  
   29  #if WIN32
   30  			int bufferSize = GetLocaleInfoA(LOCALE_USER_DEFAULT, LOCALE_SSHORTDATE, nullptr, 0);
   31  			if (bufferSize > 0)
   32  			{
   33  				// Allocate a buffer to store the short date format
   34  				char* buffer = new char[bufferSize];
   35  
   36  				char dateTimeStr[64];
   37  				SYSTEMTIME st;
   38  				GetDateFormatA(LOCALE_USER_DEFAULT, DATE_SHORTDATE, NULL, NULL, dateTimeStr, sizeof(dateTimeStr));
   39  
   40  				// Get the short date format
   41  				if (GetLocaleInfoA(LOCALE_USER_DEFAULT, LOCALE_SSHORTDATE, buffer, bufferSize) > 0)
   42  				{
   43  					ret = buffer;
   44  
   45  					if (ret.find("yyyy") != std::string::npos)
   46  						ret = Utils::String::replace(ret, "yyyy", "%Y");
   47  					else
   48  						ret = Utils::String::replace(ret, "yy", "%y");
   49  
   50  					if (ret.find("MM") != std::string::npos)
   51  						ret = Utils::String::replace(ret, "MM", "%m");
   52  					else
   53  						ret = Utils::String::replace(ret, "M", "%m"); // %#m
   54  
   55  					if (ret.find("dd") != std::string::npos)
   56  						ret = Utils::String::replace(ret, "dd", "%d");
   57  					else
   58  						ret = Utils::String::replace(ret, "d", "%d");
   59  
   60  					if (ret.find("tt") != std::string::npos)
   61  						ret = Utils::String::replace(ret, "tt", "%p");
   62  					else
   63  						ret = Utils::String::replace(ret, "t", "%p");
   64  
   65  					if (ret.find("HH") != std::string::npos)
   66  						ret = Utils::String::replace(ret, "HH", "%H");
   67  					else
   68  						ret = Utils::String::replace(ret, "H", "%H");
   69  
   70  					if (ret.find("hh") != std::string::npos)
   71  						ret = Utils::String::replace(ret, "hh", "%I");
   72  					else
   73  						ret = Utils::String::replace(ret, "h", "%I");
   74  
   75  					ret = Utils::String::replace(ret, "mm", "%M");
   76  					ret = Utils::String::replace(ret, "ss", "%S");
   77  				}
   78  
   79  				if (includeHours && ret.find("%H") == std::string::npos)
   80  				{
   81  					if (Settings::ClockMode12())
   82  						ret += " %I:%M %p";
   83  					else
   84  						ret += " %H:%M";
   85  				}
   86  
   87  				delete[] buffer;
   88  			}
   89  #elif defined(__linux__)
   90  			char* date = nl_langinfo(D_FMT);
   91  			if (date)
   92  				ret = date;
   93  #endif
   94  
   95  			if (ret.empty())
   96  			{
   97  				if (includeHours)
   98  				{
   99  					if (Settings::ClockMode12())
  100  						ret = "%m/%d/%Y %I:%M %p";
  101  					else
  102  						ret = "%m/%d/%Y %H:%M";
  103  				}
  104  				else 
  105  					ret = "%m/%d/%Y";
  106  			}
  107  
  108  			if (includeHours)
  109  				valueWithHours = ret;
  110  			else
  111  				value = ret;
  112  
  113  			return ret;
  114  		}
  115  
  116  		DateTime DateTime::now()
  117  		{
  118  			return Utils::Time::DateTime(Utils::Time::now());
  119  		}
  120  
  121  		DateTime::DateTime()
  122  		{
  123  			mTime       = 0;
  124  			mTimeStruct = { 0, 0, 0, 1, 0, 0, 0, 0, -1 };
  125  			mIsoString  = "00000000T000000";
  126  
  127  		} // DateTime::DateTime
  128  
  129  		DateTime::DateTime(const time_t& _time)
  130  		{
  131  			setTime(_time);
  132  
  133  		} // DateTime::DateTime
  134  
  135  		DateTime::DateTime(const tm& _timeStruct)
  136  		{
  137  			setTimeStruct(_timeStruct);
  138  
  139  		} // DateTime::DateTime
  140  
  141  		DateTime::DateTime(const std::string& _isoString)
  142  		{
  143  			setIsoString(_isoString);
  144  
  145  		} // DateTime::DateTime
  146  
  147  		DateTime::~DateTime()
  148  		{
  149  
  150  		} // DateTime::~DateTime
  151  
  152  		void DateTime::setTime(const time_t& _time)
  153  		{
  154  			try
  155  			{
  156  				mTime = (_time < 0) ? 0 : _time;
  157  				mTimeStruct = *localtime(&mTime);
  158  				mIsoString = timeToString(mTime);
  159  			}
  160  			catch (...)
  161  			{
  162  				mTime = 0;
  163  				mTimeStruct = { 0, 0, 0, 1, 0, 0, 0, 0, -1 };
  164  				mIsoString = "00000000T000000";
  165  			}
  166  		} // DateTime::setTime
  167  
  168  		void DateTime::setTimeStruct(const tm& _timeStruct)
  169  		{
  170  			setTime(mktime((tm*)&_timeStruct));
  171  
  172  		} // DateTime::setTimeStruct
  173  
  174  		void DateTime::setIsoString(const std::string& _isoString)
  175  		{
  176  			setTime(stringToTime(_isoString));
  177  
  178  		} // DateTime::setIsoString
  179  
  180  		double	DateTime::elapsedSecondsSince(const DateTime& _since)
  181  		{
  182  			return difftime(mTime, _since.mTime);
  183  		}
  184  
  185  		std::string DateTime::toLocalTimeString()
  186  		{
  187  			time_t     clockNow = getTime();
  188  			struct tm  clockTstruct = *localtime(&clockNow);
  189  
  190  			// The date as the locale writes it, then the hour as SHOW CLOCK IN
  191  			// 12-HOUR FORMAT says, read at each call (fork #195, D-UI-058). It
  192  			// was a fixed "%x %R": a 24-hour time whatever the switch said,
  193  			// while the clock in the corner and the cloud rows' LAST lines
  194  			// followed it -- so the SAVE STATE MANAGER's "09/13/2026 09:07",
  195  			// a Sunday-morning file, was read as 9:07 pm on a Monday night.
  196  			// The words are clockText's, which es-unit-tests holds to them;
  197  			// this is the shell that asks the locale and the setting. Both
  198  			// strftime results are taken by their returned length: an empty
  199  			// %p (French) returns 0 and says nothing about the buffer.
  200  			char dateBuf[64];
  201  			const size_t dateLen = strftime(dateBuf, sizeof(dateBuf), "%x", &clockTstruct);
  202  
  203  			return std::string(dateBuf, dateLen) + " " + localClockText(clockTstruct);
  204  		}
  205  
  206  		// The time half alone, as toLocalTimeString writes it after the date.
  207  		std::string DateTime::localClockText(const tm& clockTstruct)
  208  		{
  209  			const bool twelveHour = Settings::ClockMode12();
  210  			char markerBuf[32];
  211  			size_t markerLen = 0;
  212  			if (twelveHour)
  213  				markerLen = strftime(markerBuf, sizeof(markerBuf), "%p", &clockTstruct);
  214  
  215  			return clockText(clockTstruct, twelveHour, std::string(markerBuf, markerLen));
  216  		}
  217  
  218  		std::string DateTime::toShortLocalDateString()
  219  		{
  220  			time_t     clockNow = getTime();
  221  			struct tm  clockTstruct = *localtime(&clockNow);
  222  			char dateBuf[64];
  223  			const size_t dateLen = strftime(dateBuf, sizeof(dateBuf), "%x", &clockTstruct);
  224  			return shortYear(std::string(dateBuf, dateLen));
  225  		}
  226  
  227  		std::string DateTime::toRelativeLocalTimeString(const std::string& todayWord, const std::string& yesterdayWord, const std::string& atWord)
  228  		{
  229  			// Both in local time, so the day boundary is the player's
  230  			// midnight (fork #195, D-UI-087, D-UI-089). The rules are
  231  			// dayRelation's and whenText's, held by es-unit-tests; this is the
  232  			// shell that asks the clock and the locale.
  233  			time_t     stampNow = getTime();
  234  			struct tm  stamp    = *localtime(&stampNow);
  235  			time_t     clockNow = now();
  236  			struct tm  today    = *localtime(&clockNow);
  237  
  238  			return whenText(dayRelation(stamp, today), toShortLocalDateString(), localClockText(stamp),
  239  			                todayWord, yesterdayWord, atWord);
  240  		}
  241  
  242  		Duration::Duration(const time_t& _time)
  243  		{
  244  			mTotalSeconds = (unsigned int)_time;
  245  			mDays         = (mTotalSeconds - (mTotalSeconds % (60*60*24))) / (60*60*24);
  246  			mHours        = ((mTotalSeconds % (60*60*24)) - (mTotalSeconds % (60*60))) / (60*60);
  247  			mMinutes      = ((mTotalSeconds % (60*60)) - (mTotalSeconds % (60))) / 60;
  248  			mSeconds      = mTotalSeconds % 60;
  249  
  250  		} // Duration::Duration
  251  
  252  		Duration::~Duration()
  253  		{
  254  
  255  		} // Duration::~Duration
  256  
  257  		time_t now()
  258  		{
  259  			time_t time;
  260  			::time(&time);
  261  			return time;
  262  
  263  		} // now
  264  
  265  		time_t stringToTime(const std::string& _string, const std::string& _format)
  266  		{
  267  			const char* s           = _string.c_str();
  268  			const char* f           = _format.c_str();
  269  			tm          timeStruct  = { 0, 0, 0, 1, 0, 0, 0, 0, -1 };
  270  			size_t      parsedChars = 0;
  271  
  272  			if(_string == "not-a-date-time")
  273  				return mktime(&timeStruct);
  274  
  275  			while(*f && (parsedChars < _string.length()))
  276  			{
  277  				if(*f == '%')
  278  				{
  279  					++f;
  280  				
  281  					switch(*f++)
  282  					{
  283  						case 'Y': // The year [1970,xxxx]
  284  						{
  285  							if((parsedChars + 4) <= _string.length())
  286  							{
  287  								timeStruct.tm_year  = (*s++ - '0') * 1000;
  288  								timeStruct.tm_year += (*s++ - '0') * 100;
  289  								timeStruct.tm_year += (*s++ - '0') * 10;
  290  								timeStruct.tm_year += (*s++ - '0');
  291  								if(timeStruct.tm_year >= 1900)
  292  									timeStruct.tm_year -= 1900;
  293  							}
  294  
  295  							parsedChars += 4;
  296  						}
  297  						break;
  298  
  299  						case 'y': // The year [1970,xxxx]
  300  						{
  301  							if ((parsedChars + 2) <= _string.length())
  302  							{
  303  								timeStruct.tm_year = (*s++ - '0') * 10;
  304  								timeStruct.tm_year += (*s++ - '0');								
  305  								if (timeStruct.tm_year < 50)
  306  									timeStruct.tm_year += 100;
  307  							}
  308  
  309  							parsedChars += 2;
  310  						}
  311  						break;
  312  
  313  						case 'm': // The month number [01,12]
  314  						{
  315  							if((parsedChars + 2) <= _string.length())
  316  							{
  317  								timeStruct.tm_mon  = (*s++ - '0') * 10;
  318  								timeStruct.tm_mon += (*s++ - '0');
  319  								if(timeStruct.tm_mon >= 1)
  320  									timeStruct.tm_mon -= 1;
  321  							}
  322  
  323  							parsedChars += 2;
  324  						}
  325  						break;
  326  
  327  						case 'd': // The day of the month [01,31]
  328  						{
  329  							if((parsedChars + 2) <= _string.length())
  330  							{
  331  								timeStruct.tm_mday  = (*s++ - '0') * 10;
  332  								timeStruct.tm_mday += (*s++ - '0');
  333  							}
  334  
  335  							parsedChars += 2;
  336  						}
  337  						break;
  338  
  339  						case 'H': // The hour (24-hour clock) [00,23]
  340  						{
  341  							if((parsedChars + 2) <= _string.length())
  342  							{
  343  								timeStruct.tm_hour  = (*s++ - '0') * 10;
  344  								timeStruct.tm_hour += (*s++ - '0');
  345  							}
  346  
  347  							parsedChars += 2;
  348  						}
  349  						break;
  350  
  351  						case 'I': // The hour (12-hour clock) [00,11]
  352  						{
  353  							if ((parsedChars + 2) <= _string.length())
  354  							{
  355  								timeStruct.tm_hour = (*s++ - '0') * 10;
  356  								timeStruct.tm_hour += (*s++ - '0');
  357  							}
  358  
  359  							parsedChars += 2;
  360  						}
  361  						break;
  362  
  363  						case 'p': // The 12-hour clock AM / PM value
  364  						{
  365  							if ((parsedChars + 2) <= _string.length())
  366  							{
  367  								if (s[0] == 'P' && timeStruct.tm_hour < 12)
  368  									timeStruct.tm_hour += 12;
  369  							}
  370  
  371  							parsedChars += 2;
  372  						}
  373  						break;
  374  
  375  						case 'M': // The minute [00,59]
  376  						{
  377  							if((parsedChars + 2) <= _string.length())
  378  							{
  379  								timeStruct.tm_min  = (*s++ - '0') * 10;
  380  								timeStruct.tm_min += (*s++ - '0');
  381  							}
  382  
  383  							parsedChars += 2;
  384  						}
  385  						break;
  386  
  387  						case 'S': // The second [00,59]
  388  						{
  389  							if((parsedChars + 2) <= _string.length())
  390  							{
  391  								timeStruct.tm_sec  = (*s++ - '0') * 10;
  392  								timeStruct.tm_sec += (*s++ - '0');
  393  							}
  394  
  395  							parsedChars += 2;
  396  						}
  397  						break;
  398  					}
  399  				}
  400  				else
  401  				{
  402  					++s;
  403  					++f;
  404  				}
  405  			}
  406  
  407  			return mktime(&timeStruct);
  408  
  409  		} // stringToTime
  410  
  411  		std::string timeToString(const time_t& _time, const std::string& _format)
  412  		{
  413  			const char* f = _format.c_str();
  414  			const tm timeStruct = *localtime(&_time);
  415  			char buf[256] = { '\0' };
  416  			char* s = buf;
  417  
  418  			while(*f)
  419  			{
  420  				if(*f == '%')
  421  				{
  422  					++f;
  423  				
  424  					switch(*f++)
  425  					{
  426  						case 'Y': // The year, including the century (1900)
  427  						{
  428  							const int year = timeStruct.tm_year + 1900;
  429  							*s++ = (char)((year - (year % 1000)) / 1000) + '0';
  430  							*s++ = (char)(((year % 1000) - (year % 100)) / 100) + '0';
  431  							*s++ = (char)(((year % 100) - (year % 10)) / 10) + '0';
  432  							*s++ = (char)(year % 10) + '0';
  433  						}
  434  						break;
  435  
  436  						case 'y': // The year, without the century
  437  						{
  438  							const int year = timeStruct.tm_year + 1900;
  439  							*s++ = (char)(((year % 100) - (year % 10)) / 10) + '0';
  440  							*s++ = (char)(year % 10) + '0';
  441  						}
  442  						break;
  443  
  444  						case 'm': // The month number [00,11]
  445  						{
  446  							const int mon = timeStruct.tm_mon + 1;
  447  							*s++ = (char)(mon / 10) + '0';
  448  							*s++ = (char)(mon % 10) + '0';
  449  						}
  450  						break;
  451  
  452  						case 'd': // The day of the month [01,31]
  453  						{
  454  							*s++ = (char)(timeStruct.tm_mday / 10) + '0';
  455  							*s++ = (char)(timeStruct.tm_mday % 10) + '0';
  456  						}
  457  						break;
  458  
  459  						case 'H': // The hour (24-hour clock) [00,23]
  460  						{
  461  							*s++ = (char)(timeStruct.tm_hour / 10) + '0';
  462  							*s++ = (char)(timeStruct.tm_hour % 10) + '0';
  463  						}
  464  						break;
  465  
  466  						case 'I': // The hour (12-hour clock) [01,12]
  467  						{
  468  							int h = timeStruct.tm_hour;
  469  							if (h >= 12)
  470  								h -= 12;
  471  							if (h == 0)
  472  								h = 12;
  473  
  474  							*s++ = (char)(h / 10) + '0';
  475  							*s++ = (char)(h % 10) + '0';
  476  						}
  477  						break;
  478  
  479  						case 'p': // AM / PM
  480  						{
  481  							*s++ = timeStruct.tm_hour < 12 ? 'A' : 'P';
  482  							*s++ = 'M';
  483  						}
  484  						break;
  485  
  486  						case 'M': // The minute [00,59]
  487  						{
  488  							*s++ = (char)(timeStruct.tm_min / 10) + '0';
  489  							*s++ = (char)(timeStruct.tm_min % 10) + '0';
  490  						}
  491  						break;
  492  
  493  						case 'S': // The second [00,59]
  494  						{
  495  							*s++ = (char)(timeStruct.tm_sec / 10) + '0';
  496  							*s++ = (char)(timeStruct.tm_sec % 10) + '0';
  497  						}
  498  						break;
  499  					}
  500  				}
  501  				else
  502  				{
  503  					*s++ = *f++;
  504  				}
  505  
  506  				*s = '\0';
  507  			}
  508  
  509  			return std::string(buf);
  510  
  511  		} // timeToString
  512  
  513  		  // transforms a number of seconds into a human readable string
  514  		std::string secondsToString(const long seconds, bool asTime)
  515  		{
  516  			if (seconds == 0)
  517  				return _("never");
  518  
  519  			if (asTime)
  520  			{
  521  				int d = 0, h = 0, m = 0, s = 0;
  522  				d = seconds / 86400;
  523  				h = (seconds / 3600) % 24;
  524  				m = (seconds / 60) % 60;
  525  				s = seconds % 60;
  526  
  527  				if (d > 0)
  528  					return Utils::String::format("%02d %02d:%02d:%02d", d, h, m, s);
  529  				else if (h > 0)
  530  					return Utils::String::format("%02d:%02d:%02d", h, m, s);
  531  
  532  				return Utils::String::format("%02d:%02d", m, s);
  533  			}
  534  
  535  			char buf[256];
  536  
  537  			int d =0, h = 0, m = 0, s = 0;
  538  			d = seconds / 86400;
  539  			h = (seconds / 3600) % 24;
  540  			m = (seconds / 60) % 60;
  541  			s = seconds % 60;
  542  			if (d > 1)
  543  			{
  544  				snprintf(buf, 256, _("%d d").c_str(), d);
  545  				if (h > 0)
  546  				{
  547  					std::string days(buf);
  548  					snprintf(buf, 256, _("%d h").c_str(), h);
  549  					if(m > 0)
  550  					{
  551  						std::string hours(buf);
  552  						snprintf(buf, 256, _("%d mn").c_str(), m);
  553  						return days + " " + hours + " " + std::string(buf);
  554  					}
  555  					return days + " " + std::string(buf);
  556  				}
  557  				else if (m > 0)
  558  				{
  559  					std::string days(buf);
  560  					snprintf(buf, 256, _("%d mn").c_str(), m);
  561  					return days + " " + std::string(buf);
  562  				}
  563  			}
  564  			else if (h > 0 || d > 0)
  565  			{
  566  				if (d > 0)
  567  					h += d * 24;
  568  
  569  				snprintf(buf, 256, _("%d h").c_str(), h);
  570  				if (m > 0)
  571  				{
  572  					std::string hours(buf);
  573  					snprintf(buf, 256, _("%d mn").c_str(), m);
  574  					return hours + " " + std::string(buf);
  575  				}
  576  			}
  577  			else if (m > 0)
  578  				snprintf(buf, 256, _("%d mn").c_str(), m);
  579  			else 
  580  				snprintf(buf, 256, _("%d sec").c_str(), s);
  581  
  582  			return std::string(buf);	
  583  		}
  584  
  585  		std::string getElapsedSinceString(const time_t& _time)
  586  		{			
  587  			if (_time == 0 || _time == -1)
  588  				return _("never");
  589  
  590  			Utils::Time::DateTime now(Utils::Time::now());
  591  			Utils::Time::Duration dur(now.getTime() - _time);
  592  
  593  			char buf[256];
  594  
  595  			if (dur.getDays() > 365)
  596  			{
  597  				unsigned int years = dur.getDays() / 365;
  598  				snprintf(buf, 256, ngettext("%d year ago", "%d years ago", years), years);
  599  			}
  600  			else if (dur.getDays() > 0)
  601  				snprintf(buf, 256, ngettext("%d day ago", "%d days ago", dur.getDays()), dur.getDays());
  602  			else if (dur.getDays() > 0)
  603  				snprintf(buf, 256, ngettext("%d day ago", "%d days ago", dur.getDays()), dur.getDays());
  604  			else if (dur.getHours() > 0)
  605  				snprintf(buf, 256, ngettext("%d hour ago", "%d hours ago", dur.getHours()), dur.getHours());
  606  			else if (dur.getMinutes() > 0)
  607  				snprintf(buf, 256, ngettext("%d minute ago", "%d minutes ago", dur.getMinutes()), dur.getMinutes());
  608  			else
  609  				snprintf(buf, 256, ngettext("%d second ago", "%d seconds ago", dur.getSeconds()), dur.getSeconds());
  610  
  611  			return std::string(buf);
  612  		}
  613  
  614  		int daysInMonth(const int _year, const int _month)
  615  		{
  616  			tm timeStruct = { 0, 0, 0, 0, _month, _year - 1900, 0, 0, -1 };
  617  			mktime(&timeStruct);
  618  
  619  			return timeStruct.tm_mday;
  620  
  621  		} // daysInMonth
  622  
  623  		int daysInYear(const int _year)
  624  		{
  625  			tm timeStruct = { 0, 0, 0, 0, 0, _year - 1900 + 1, 0, 0, -1 };
  626  			mktime(&timeStruct);
  627  
  628  			return timeStruct.tm_yday + 1;
  629  
  630  		} // daysInYear
  631  
  632  	} // Time::
  633  
  634  } // Utils::
```

## src/utils/TimeUtil.h (whole, fork-modified, at the pin)

```text
    1  #pragma once
    2  #ifndef ES_CORE_UTILS_TIME_UTIL_H
    3  #define ES_CORE_UTILS_TIME_UTIL_H
    4  
    5  #include <string>
    6  #include <time.h>
    7  
    8  namespace Utils
    9  {
   10  	namespace Time
   11  	{
   12  		static int NOT_A_DATE_TIME = 0;
   13  
   14  		class DateTime
   15  		{
   16  		public:
   17  			 static DateTime now();
   18  
   19  			 DateTime();
   20  			 DateTime(const time_t& _time);
   21  			 DateTime(const tm& _timeStruct);
   22  			 DateTime(const std::string& _isoString);
   23  			~DateTime();
   24  
   25  			const bool operator<           (const DateTime& _other) const { return (mTime <  _other.mTime); }
   26  			const bool operator<=          (const DateTime& _other) const { return (mTime <= _other.mTime); }
   27  			const bool operator>           (const DateTime& _other) const { return (mTime >  _other.mTime); }
   28  			const bool operator>=          (const DateTime& _other) const { return (mTime >= _other.mTime); }
   29  			           operator time_t     ()                       const { return mTime; }
   30  			           operator tm         ()                       const { return mTimeStruct; }
   31  			           operator std::string()                       const { return mIsoString; }
   32  
   33  			void               setTime      (const time_t& _time);
   34  			const time_t&      getTime      () const { return mTime; }
   35  			void               setTimeStruct(const tm& _timeStruct);
   36  			const tm&          getTimeStruct() const { return mTimeStruct; }
   37  			void               setIsoString (const std::string& _isoString);
   38  			const std::string& getIsoString () const { return mIsoString; }
   39  			std::string		   toLocalTimeString();
   40  			// When this was, as a save state tile says it (fork #195, D-UI-089):
   41  			// "TODAY at 17:07", "YESTERDAY at 14:03", "09/24/26 at 14:03" -- the
   42  			// caller passes the three translated words; the date is the
   43  			// locale's with a two-digit year; the time follows the 12-hour
   44  			// switch (D-UI-058).
   45  			std::string		   toRelativeLocalTimeString(const std::string& todayWord, const std::string& yesterdayWord, const std::string& atWord);
   46  			// The locale's date of this stamp with a two-digit year, and the
   47  			// time half alone, for callers that compose their own line.
   48  			std::string		   toShortLocalDateString();
   49  			static std::string localClockText(const tm& clockTstruct);
   50  
   51  			double			   elapsedSecondsSince(const DateTime& _since);
   52  
   53  			bool				isValid() { return mTime != 0; }
   54  
   55  		private:
   56  
   57  			time_t      mTime;
   58  			tm          mTimeStruct;
   59  			std::string mIsoString;
   60  
   61  		}; // DateTime
   62  
   63  		class Duration
   64  		{
   65  		public:
   66  
   67  			 Duration(const time_t& _time);
   68  			~Duration();
   69  
   70  			unsigned int getDays   () const { return mDays; }
   71  			unsigned int getHours  () const { return mHours; }
   72  			unsigned int getMinutes() const { return mMinutes; }
   73  			unsigned int getSeconds() const { return mSeconds; }
   74  
   75  		private:
   76  
   77  			unsigned int mTotalSeconds;
   78  			unsigned int mDays;
   79  			unsigned int mHours;
   80  			unsigned int mMinutes;
   81  			unsigned int mSeconds;
   82  
   83  		}; // Duration
   84  
   85  		time_t      now         ();
   86  		time_t      stringToTime(const std::string& _string, const std::string& _format = "%Y%m%dT%H%M%S");
   87  		std::string timeToString(const time_t& _time, const std::string& _format = "%Y%m%dT%H%M%S");
   88  		int         daysInMonth (const int _year, const int _month);
   89  		int         daysInYear  (const int _year);
   90  		std::string secondsToString(const long seconds, bool asTime = false);
   91  
   92  		std::string getSystemDateFormat(bool includeHours = false);
   93  		std::string getElapsedSinceString(const time_t& _time);
   94  
   95  	} // Time::
   96  
   97  } // Utils::
   98  
   99  #endif // ES_CORE_UTILS_TIME_UTIL_H
```

## src/utils/ZipFile.cpp `:251-267` (an excerpt, upstream-carried, at the pin)

```text
  251  		}
  252  
  253  		bool ZipFile::extract(const std::string &member, const std::string &path, bool pathIsFullPath)
  254  		{
  255  			if (mZipFile == nullptr)
  256  				return false;
  257  
  258  			auto fullPath = join_path({ path, member });
  259  			return mz_zip_reader_extract_file_to_file(mZipArchive, getInternalFilename(member).c_str(), (pathIsFullPath ? path : fullPath).c_str(), 0);
  260  		}
  261  
  262  		struct OpaqueWrapper
  263  		{
  264  			zip_callback callback;
  265  			void* opaque;
  266  		};
  267  
```

## The first reader's 02-forward-audit.md (whole)

# Forward audit: M6.P2 T36, EmulationStation's utilities, resources and renderers (#683)

- **At:** the pin `16dbac5211eea7e70db7394372033be2be7df829` (ES) and `a5fbd75d61` (distribution, stage A's tip). Stage B, the T1 session (Opus 5.5, high).
- **The 58 paths:** `es-core/src/{utils,resources,renderers}/**` less `utils/AtomicFileUtil.*` (`stage-a/paths.txt`).
- **Generated sections:** each generated table sits between `<!-- gen:NAME -->` markers. It is written by `tools/t36-tables.py --write 02-forward-audit.md`, read back by `--check`, and ends with its own "generated, asserted" line. The script exits 1 before writing when a count drifts. Its constructed drifts are `stage-b/tables-drift.out`.
- **What stage B did not do:** no case ran (stage C), no guest started (the window is asked for on #683), and no fix was made (stage E, under a stream brief).
- **`proved:` values:**
  - `tree`: read at the pin.
  - `tool-run`: a stage-A run in `stage-a/runs.out`.
  - `pending stage C` / `pending window`: owed.

## Coverage

All 58 paths. Each row gives its provenance against the merge base, its inventory tier, whether its blob is ROCKNIX master's, batocera's commits on it since `1750dded8c`, and the section that reads it.

<!-- gen:coverage -->
| Path | Lines (`grep -c ''`) | Against the merge base `cada856d86` | Inventory tier | Blob = ROCKNIX `f6c542872e` | Batocera commits since `1750dded8c` | Read under (`02` §) |
| --- | --- | --- | --- | --- | --- | --- |
| `es-core/src/renderers/GlExtensions.cpp` | 140 | upstream-carried | upstream-carried | yes | 0 | the device reads, the renderers and the words; the structure |
| `es-core/src/renderers/GlExtensions.h` | 88 | upstream-carried | upstream-carried | yes | 0 | the device reads, the renderers and the words; the structure |
| `es-core/src/renderers/Renderer.cpp` | 1170 | upstream-carried | upstream-carried | yes | 2 | the device reads, the renderers and the words; the structure |
| `es-core/src/renderers/Renderer.h` | 263 | upstream-carried | upstream-carried | yes | 0 | the device reads, the renderers and the words; the structure |
| `es-core/src/renderers/Renderer_GL21.cpp` | 459 | upstream-carried | upstream-carried | yes | 0 | the structure (no image compiles the body) |
| `es-core/src/renderers/Renderer_GL21.h` | 53 | upstream-carried | upstream-carried | yes | 0 | the structure (no image compiles the body) |
| `es-core/src/renderers/Renderer_GLES10.cpp` | 422 | upstream-carried | upstream-carried | yes | 0 | the structure (no image compiles the body) |
| `es-core/src/renderers/Renderer_GLES10.h` | 53 | upstream-carried | upstream-carried | yes | 0 | the structure (no image compiles the body) |
| `es-core/src/renderers/Renderer_GLES20.cpp` | 1420 | upstream-carried | upstream-carried | yes | 0 | the structure (no image compiles the body) |
| `es-core/src/renderers/Renderer_GLES20.h` | 67 | upstream-carried | upstream-carried | yes | 0 | the structure (no image compiles the body) |
| `es-core/src/renderers/Renderer_GLES30.cpp` | 2291 | upstream-carried | upstream-carried | yes | 1 | the device reads, the renderers and the words; the structure |
| `es-core/src/renderers/Renderer_GLES30.h` | 69 | upstream-carried | upstream-carried | yes | 0 | the device reads, the renderers and the words; the structure |
| `es-core/src/renderers/Shader.cpp` | 642 | upstream-carried | upstream-carried | yes | 1 | the device reads, the renderers and the words; the structure |
| `es-core/src/renderers/Shader.h` | 146 | upstream-carried | upstream-carried | yes | 1 | the device reads, the renderers and the words; the structure |
| `es-core/src/resources/Font.cpp` | 1311 | fork-modified | fork-own | no | 4 | the texture and font caches (the font) |
| `es-core/src/resources/Font.h` | 217 | fork-modified | fork-own | no | 1 | the texture and font caches (the font) |
| `es-core/src/resources/ResourceManager.cpp` | 258 | upstream-carried | upstream-carried | yes | 0 | the texture and font caches |
| `es-core/src/resources/ResourceManager.h` | 64 | upstream-carried | upstream-carried | yes | 0 | the texture and font caches |
| `es-core/src/resources/TabStops.h` | 49 | fork-added | fork-own | no | 0 | the texture and font caches (the font) |
| `es-core/src/resources/TextureData.cpp` | 739 | fork-modified | fork-own | no | 2 | the texture and font caches |
| `es-core/src/resources/TextureData.h` | 126 | upstream-carried | upstream-carried | yes | 0 | the texture and font caches |
| `es-core/src/resources/TextureDataManager.cpp` | 381 | upstream-carried | upstream-carried | yes | 0 | the texture and font caches |
| `es-core/src/resources/TextureDataManager.h` | 108 | upstream-carried | upstream-carried | yes | 0 | the texture and font caches |
| `es-core/src/resources/TextureResource.cpp` | 348 | upstream-carried | upstream-carried | yes | 0 | the texture and font caches |
| `es-core/src/resources/TextureResource.h` | 74 | upstream-carried | upstream-carried | yes | 0 | the texture and font caches |
| `es-core/src/utils/CommandLineUtil.h` | 104 | fork-added | fork-own | no | 0 | the structure (fork files whole) |
| `es-core/src/utils/ConcurrentVector.h` | 92 | upstream-carried | upstream-carried | yes | 0 | the texture and font caches (threads, L-17); the structure |
| `es-core/src/utils/Delegate.h` | 27 | upstream-carried | upstream-carried | yes | 0 | the structure |
| `es-core/src/utils/FileSystemUtil.cpp` | 1805 | upstream-carried | upstream-carried | yes | 1 | the file cache; the paths; the writes and reads |
| `es-core/src/utils/FileSystemUtil.h` | 103 | upstream-carried | upstream-carried | yes | 0 | the file cache; the paths; the writes and reads |
| `es-core/src/utils/HtmlColor.cpp` | 248 | upstream-carried | upstream-carried | yes | 0 | the structure |
| `es-core/src/utils/HtmlColor.h` | 18 | upstream-carried | upstream-carried | yes | 0 | the structure |
| `es-core/src/utils/MathExpr.cpp` | 1016 | upstream-carried | upstream-carried | yes | 0 | the device reads, the renderers and the words (the `_(` line) |
| `es-core/src/utils/MathExpr.h` | 75 | upstream-carried | upstream-carried | yes | 0 | the device reads, the renderers and the words (the `_(` line) |
| `es-core/src/utils/OfflineProxyUrl.cpp` | 21 | fork-added | fork-own | no | 0 | the structure (fork files whole) |
| `es-core/src/utils/OfflineProxyUrl.h` | 40 | fork-added | fork-own | no | 0 | the structure (fork files whole) |
| `es-core/src/utils/Platform.cpp` | 956 | fork-modified | fork-own | no | 1 | the processes; the device reads |
| `es-core/src/utils/Platform.h` | 100 | fork-modified | fork-own | no | 0 | the processes; the device reads |
| `es-core/src/utils/Randomizer.cpp` | 53 | upstream-carried | upstream-carried | yes | 0 | the structure |
| `es-core/src/utils/Randomizer.h` | 19 | upstream-carried | upstream-carried | yes | 0 | the structure |
| `es-core/src/utils/StringListLock.cpp` | 61 | upstream-carried | upstream-carried | yes | 0 | the texture and font caches (threads, L-17); the structure |
| `es-core/src/utils/StringListLock.h` | 30 | upstream-carried | upstream-carried | yes | 0 | the texture and font caches (threads, L-17); the structure |
| `es-core/src/utils/StringUtil.cpp` | 1706 | fork-modified | fork-own | no | 0 | the device reads, the renderers and the words (case helpers); the processes (`shellQuote`, `maskSecrets`) |
| `es-core/src/utils/StringUtil.h` | 96 | fork-modified | fork-own | no | 0 | the device reads, the renderers and the words (case helpers); the processes (`shellQuote`, `maskSecrets`) |
| `es-core/src/utils/ThreadPool.cpp` | 230 | upstream-carried | upstream-carried | yes | 0 | the texture and font caches (threads, L-17); the structure |
| `es-core/src/utils/ThreadPool.h` | 77 | upstream-carried | upstream-carried | yes | 0 | the texture and font caches (threads, L-17); the structure |
| `es-core/src/utils/TimeText.cpp` | 83 | fork-added | fork-own | no | 0 | the device reads, the renderers and the words |
| `es-core/src/utils/TimeText.h` | 57 | fork-added | fork-own | no | 0 | the device reads, the renderers and the words |
| `es-core/src/utils/TimeUtil.cpp` | 634 | fork-modified | fork-own | no | 0 | the device reads, the renderers and the words |
| `es-core/src/utils/TimeUtil.h` | 99 | fork-modified | fork-own | no | 0 | the device reads, the renderers and the words |
| `es-core/src/utils/Uri.h` | 144 | upstream-carried | upstream-carried | yes | 0 | the structure |
| `es-core/src/utils/VectorEx.h` | 170 | upstream-carried | upstream-carried | yes | 0 | the structure |
| `es-core/src/utils/ZipFile.cpp` | 369 | upstream-carried | upstream-carried | yes | 0 | the writes and reads; the structure (reading scope) |
| `es-core/src/utils/ZipFile.h` | 51 | upstream-carried | upstream-carried | yes | 0 | the writes and reads; the structure (reading scope) |
| `es-core/src/utils/han.h` | 20923 | upstream-carried | upstream-carried | yes | 0 | the structure (reading scope) |
| `es-core/src/utils/md5.cpp` | 369 | upstream-carried | upstream-carried | yes | 0 | the structure |
| `es-core/src/utils/md5.h` | 95 | upstream-carried | upstream-carried | yes | 0 | the structure |
| `es-core/src/utils/zip_file.hpp` | 10011 | upstream-carried | upstream-carried | yes | 0 | the writes and reads; the structure (reading scope) |

generated, asserted: 58 rows (`tools/t36-tables.py --print coverage`)

Totals: fork-added 6, fork-modified 9, upstream-carried 43; inventory fork-own 15, upstream-carried 43; 43 of 58 blobs identical to ROCKNIX's master; batocera 13 commits on 9 files since `1750dded8c`.
<!-- /gen:coverage -->

## The leads

- **The table:** L-01 to L-18 are the brief's (R2 and R3). L-19 is stage B's own (§ The file cache).
- **The floor:** 3.1 to 3.25 are the brief's floor; 3.26 is stage B's case for L-19. Every case runs at stage C.
- **Family:** a lead's family is the brief's natural home for it (§ 4's opening paragraph).

<!-- gen:leads -->
| Lead | Lines at the pin | Family | Owner | Disposition at stage B | proved: |
| --- | --- | --- | --- | --- | --- |
| L-01 | `utils/StringUtil.cpp:357-362`, `:398-403` against `:352-356`, `:393-397`; tables `:76`, `:93`, `:153`, `:170`; lookup `:184-200` | a player sentence | T36 | case 3.1 at stage C (FAIL at the pin expected); a fix only under a stream brief | tree |
| L-02 | `utils/FileSystemUtil.cpp:1369-1379`, `:1400-1427` | a write's claim | T20 (#1177, `d9afa5c7c`) -- collision | control 3.4 at stage C, never re-fixed here; § The merge debt | tree |
| L-03 | `utils/FileSystemUtil.cpp:1451-1452`, `:1454-1455`, `:1463`; `:1472-1474`, `:1492`, `:1500-1504` | a write's claim | `renameFile`: T21 (#1191, `f7c16144d`) -- collision; `copyFile`: T36 | case 3.2 at stage C; `copyFile`'s half this slice's (rule 6) | tree |
| L-04 | `utils/FileSystemUtil.cpp:1429-1446`; `es-app/src/ThreadedCloudSync.cpp:943-948` (T18's) | a write's claim | the pause (#1186, T21 PL-20); call sites their owners' | text case 3.3; the return or the supersession put to the stage-D pause | tree |
| L-05 | `utils/Platform.cpp:40`, `:52`, `:162-168` | a process's contract | T36 (ruling (j): T35's PL-03 fix is `Scripting`'s) | 3.5's two host rcs at stage A; G-07 reads `SigIgn` first (errata), then the image's shell and wrapper | tree |
| L-06 | `utils/Platform.cpp:891-905` | a process's contract | T26 (#1225, `a5d2d3756`) -- collision | control 3.9 at stage C, never re-fixed here; § The merge debt | tree |
| L-07 | `resources/Font.cpp:1238`, `:1255`, `:165-166`, `:99-101` | a layout computed from a moving number | T36 | case 3.16 at stage C; G-02 and G-06 frames | tree |
| L-08 | `resources/Font.cpp:107`, `:115-117`, `:420-421`; `es-code-traps.md:118`; T34 L-02 (`es-core-components.md:597`) | a layout computed from a moving number | the coordinator's rule sweep (erratum against `es-code-traps.md:118`); T34 PL-17 beside it | positive 3.8 at stage C; recorded as a rule erratum | tree |
| L-09 | `resources/Font.cpp:728-731`, `:734-745`; the fork's `getTabStops`/`sizeTabbedText` `:833-941`; `:1044-1078` | a layout computed from a moving number | T36 | case 3.17 at stage C | tree |
| L-10 | `resources/TextureData.cpp:615-645`, `:670-725` against `:92-195` (`:95` the lock) | a lifetime or a thread | T36 | TSan case 3.11 at stage C | tree |
| L-11 | `resources/TextureDataManager.cpp:231-235`, `:252-253`, `:284`; `es-app/src/views/SystemView.cpp:198`, `:226` (T32's) | a lifetime or a thread | T36 | teardown case 3.12 at stage C | tree |
| L-12 | `utils/FileSystemUtil.cpp:277-282`, `:161-162`, `:183-198` | a read of a file another process writes | T36 (ruling (h): the cache's fix is T36's, T35's 3.11 the case) | positive 3.13 at stage C; T35's 3.11 re-run at T35's tips (ruling (h) as (a)) | tree |
| L-13 | `utils/Platform.cpp:853-880` | a process's contract | the coordinator's rule sweep (erratum against `es-native-ui.md:103`); #1220 the callers' | text case 3.7 at stage C; recorded as a rule erratum | tree |
| L-14 | `utils/StringUtil.cpp:446-804` (the `=` test inside `maskSecrets`) | a player's secret in a log | T36 | case 3.10 at stage C, its value built at run time | tree |
| L-15 | `utils/FileSystemUtil.cpp:1766-1797` | a lifetime or a thread | T36 | ASan case 3.6 at stage C | tree |
| L-16 | `utils/FileSystemUtil.cpp:1089-1120` | a write's claim | T36 | case 3.15 at stage C | tree |
| L-17 | `resources/Font.cpp:30-31`, `:177`, `:417`; `resources/TextureResource.cpp:12`, `:146`; `renderers/` | a lifetime or a thread | T36 | TSan programs 3.25 at stage C; the threads named in § The texture and font caches | tree |
| L-18 | `utils/Platform.cpp:235-237` | a lifetime or a thread | T36 | text case 3.24 at stage C (recorded) | tree |
| L-19 | `utils/FileSystemUtil.cpp:1067`, `:1080`, `:1084` (stage B's read) | a read of a file another process writes | T36 (new at stage B) | case 3.26 at stage C (FAIL at the pin expected); reaches #1263's `TextureData.cpp:336-339` | tree |

generated, asserted: 19 rows (`tools/t36-tables.py --print leads`)

| Case | At the pin | Function | Status | proved: |
| --- | --- | --- | --- | --- |
| 3.1 | `utils/StringUtil.cpp:357-362`, `:398-403`; tables `:76`, `:93`, `:153`, `:170` | `toUpper`, `toLower` in `es-unit-tests` | stage C | pending stage C |
| 3.2 | `utils/FileSystemUtil.cpp:1451-1455`, `:1463`; `:1472-1474`, `:1492`, `:1500-1504` | `renameFile`, `copyFile`, `FileSystemUtil.cpp` linked whole (T21's `es-fs-tests` shape) | stage C | pending stage C |
| 3.3 | `utils/FileSystemUtil.cpp:1429-1446` | `writeAllText` | stage C | pending stage C |
| 3.4 | `utils/FileSystemUtil.cpp:1369-1379`, `:1400-1427` | `readAllText`, `readAllLines` | stage C | pending stage C |
| 3.5 | `utils/Platform.cpp:162-164` | the wrap's literal, run by the host's shell | run at stage A: `seq 400 rc=0`, `seq 200000 rc=141` on `/usr/bin/dash` (`stage-a/runs.out`); G-07 the image's | tool-run |
| 3.6 | `utils/FileSystemUtil.cpp:1758-1798` (`:1773`, `:1775`, `:1788`, `:1797`) | `preloadFileSystemCache` under ASan | stage C | pending stage C |
| 3.7 | `utils/Platform.cpp:853-880` (`:879`) | `runSystemCommand`, lifted as text | stage C | pending stage C |
| 3.8 | `resources/Font.cpp:107`, `:115-117`, `:420-421`, `:754-757` | `getHeight` (FreeType and renderer stand-ins) | stage C | pending stage C |
| 3.9 | `utils/Platform.cpp:891-905` | `GetShOutput`, extracted | stage C | pending stage C |
| 3.10 | `utils/StringUtil.cpp:446-804` | `maskSecrets` in `es-unit-tests` (`MaskSecretsTests.cpp` exists) | stage C | pending stage C |
| 3.11 | `resources/TextureData.cpp:615-645`, `:670-725` against `:92-195` | a `san tsan-...` stand-in | stage C | pending stage C |
| 3.12 | `resources/TextureDataManager.cpp:215-235`, `:252-253`, `:284` | `TextureLoader`'s teardown, with a timeout | stage C | pending stage C |
| 3.13 | `utils/FileSystemUtil.cpp:48-341`, `:1122-1147`, `:161-162` | the cache, extracted in T35's `fs_cache`/`fs_exists` shape | stage C | pending stage C |
| 3.14 | T35's `window-input-tests` case 3.11 at T35's tip (`InputManager.cpp:1187` with `FileSystemUtil.cpp`) | re-run unchanged, never edited (ruling (h)) | re-run at stage C from T35's tips of that minute, named with the time and T35's stage (ruling (h) as (a)); again at the hand-back | pending stage C |
| 3.15 | `utils/FileSystemUtil.cpp:1089-1120` | `createDirectory` | stage C | pending stage C |
| 3.16 | `resources/Font.cpp:99`, `:161-165`, `:1238`, `:1255`; `Renderer.cpp:1149` doubled | the scaling, extracted | stage C | pending stage C |
| 3.17 | `resources/Font.cpp:714-752`, `:1044-1078` | `sizeText` against the cache's last vertex (stand-ins) | stage C | pending stage C |
| 3.18 | `utils/StringUtil.cpp:426-444` | `shellQuote` in `es-unit-tests` | stage C | pending stage C |
| 3.19 | `getEscapedPath` (`FileSystemUtil.cpp`) | linked whole | run at stage C; its output is held (D-WORKFLOW-215), only a neutral line in public | pending stage C |
| 3.20 | `getCanonicalPath` (`:726`, T2's line) | linked whole, ASan | run at stage C; its output is held (D-WORKFLOW-215), only a neutral line in public | pending stage C |
| 3.21 | the relative path (`:986`) | linked whole | stage C | pending stage C |
| 3.22 | `utils/TimeUtil.cpp:514-588` | `LocaleES` and `Settings` doubles | stage C | pending stage C |
| 3.23 | `resources/TextureDataManager.cpp:135-170` | `cleanupVRAM`, extracted | stage C | pending stage C |
| 3.24 | `utils/Platform.cpp:235-237` | `quitES`, lifted as text | stage C | pending stage C |
| 3.25 | `FileSystemUtil.cpp:331-332` (`shared_mutex`); `ThreadPool.cpp:26`, `:84`, `:91`; `StringListLock.cpp`; `ConcurrentVector.h` | `san()` TSan programs (R3 § 6 item 2) | stage C | pending stage C |
| 3.26 | `utils/FileSystemUtil.cpp:1059-1087` | `removeFile`, linked whole | new at stage B (L-19): `writeAllText(p)`; `exists(p)`; `removeFile(p)`; `CHECK_FALSE(exists(p))` -- FAIL at the pin expected | pending stage C |

generated, asserted: 26 rows (`tools/t36-tables.py --print leads`)
<!-- /gen:leads -->

**The three holds.** Stage B's two named reads were the archive extraction path with its caller read whole, and the scoped lead of ruling (k) on `getCanonicalPath`'s callers. Both were weighed under D-WORKFLOW-215. The Q3 read of `getEscapedPath`'s list, made while writing § The paths, was weighed the same way. **All three met the test.**
- Their records are off the tree at `/workspace/tmp/m6-t36/held/` (directory mode 700, files mode 600), with their sha256 values in `SHA256SUMS` there and in `00`.
- Nothing more about them is written on the tree or in public. Cases 3.19 and 3.20 run at stage C with their output written to the held directory, not here.

## The file cache

The cache is an `unordered_map<size_t, FileCache>` keyed by `std::hash` of the generic path, under one `shared_mutex` (`FileSystemUtil.cpp:331-337`).
- **Reads:** reads go through it only while `Settings::UseFileCache()` (`:203`). A miss is stat'ed with no lock held and stored (`:213-215`). A directory a listing has walked answers `absent` for every name it did not list, without a stat (`:277-282`, L-12).
- **Refresh:** `exists(p, false)` and the uncached `is*` fallbacks are the one path that rewrites an entry (`fromStat64`, `:161-162`).
- **The key:** the key is the hash, not the path. Two paths whose hashes collide share one answer. That needs a 64-bit collision; it is recorded as the contract, not as a lead.

<!-- gen:filecache -->
| Entry point | At the pin | Lock | What it does | Its answer to a file another process wrote |
| --- | --- | --- | --- | --- |
| `FileCache::queryCacheEntry` | `:201` | shared, then unique for the insert | a hit answered under the shared lock; a miss stat'ed with no lock (`statKey`) and stored by `insertEntry` | the entry stands until an erase or the reset: a file created, removed or rewritten outside is not seen |
| `FileCache::insertEntry` | `:313` | unique (the caller's) | re-checks the key, then the parent's wildcard, then stores the stat | a listed parent stores `absent` without the stat it made (L-12) |
| `FileCache::getCacheEntry` | `:268` | shared (the caller's) | the key, else the parent's `/*` wildcard as a static `absent` | a listed directory answers `absent` for every name not listed |
| `FileCache::fromStat64` | `:138` | unique, after an unlocked `stat64` | overwrites the entry with the stat it made (`mFileCache[...] = cache`), with no `UseFileCache` gate | the only path that refreshes an entry: `exists(p, false)` and the uncached `is*` fallbacks |
| `FileCache::add` | `:168` | unique | a listing's entries and its `/*` wildcard (`getDirContent`, `getDirectoryFiles`) | a listing's snapshot; `_symlink` set only here, from `d_type` |
| `FileCache::remove` | `:183` | unique | erases the key and every ancestor's `/*` wildcard | the writers below call it; nothing outside ES does |
| `FileCache::resetCache / FileSystemCache::reset()` | `:258` | unique | clears the whole map | the only way a remembered answer about an outside write goes |
| `FileSystemCache::reset(file)` | `:348` | unique (through `remove`) | erases one key and its ancestors' wildcards | a caller that knows the path can drop it |
| `FileCache::isCached` | `:226` | shared | the key or the parent's wildcard present; never stats | says only that an answer is remembered |

generated, asserted: 9 rows (`tools/t36-tables.py --print filecache`)

| Writer | Erase lines | Lock | Order, read from the source |
| --- | --- | --- | --- |
| `removeDirectory` | `:1051` | unique (inside `remove`) | erase, then `rmdir`; nothing re-reads between |
| `removeFile` | `:1067` | unique (inside `remove`) | **erase, then `isDirectory(_path)` re-stats and stores `exists` (`:1080`), then `unlink` (`:1084`): the deleted path is left cached as present (L-19)** |
| `createDirectory` | `:1097` | unique (inside `remove`) | `exists(path, false)` rewrites, erase, then `mkdir`; the recursion's parents the same |
| `writeAllText` | `:1445` | unique (inside `remove`) | erase after `fclose`; skipped when `fopen` fails (nothing written) |
| `renameFile` | `:1457`, `:1458` | unique (inside `remove`) | erase both after `exists(dst, false)` and `removeFile(dst)`; the rename after the erase |
| `copyFile` | `:1506`, `:1507` | unique (inside `remove`) | erase both after the copy; skipped on an open failure |

generated, asserted: 6 rows (`tools/t36-tables.py --print filecache`)

| Function | Line | Lock | Kind | Erases |
| --- | --- | --- | --- | --- |
| `getDirContent` | `:364` | unique | a listing's write | -- |
| `getDirContent` | `:433` | unique | a listing's write | -- |
| `getDirectoryFiles` | `:479` | unique | a listing's write | -- |
| `getDirectoryFiles` | `:575` | unique | a listing's write | -- |
| `exists` | `:1145` | unique | a stat's write | -- |
| `isRegularFile` | `:1173` | unique | a stat's write | -- |
| `isDirectory` | `:1196` | unique | a stat's write | -- |
| `isDirectory` | `:1201` | unique | a stat's write | -- |
| `isSymlink` | `:1230` | unique | a stat's write | -- |

generated, asserted: 9 rows (`tools/t36-tables.py --print filecache`)

| Cited by | Line | The pin's function at that line | Image | The pin's text at that line |
| --- | --- | --- | --- | --- |
| T34's brief | `:144` | `fromStat64` | WIN32 only | `mFileCache.try_emplace(hashPath(key), ret == 0, ret == 0 && S_ISDIR(in` |
| T34's brief | `:185` | `remove` | built | `if (!Settings::UseFileCache())` |
| T34's brief | `:195` | `remove` | built | `mFileCache.erase(hashPath(parent + "/*"));` |
| T34's brief | `:203` | `queryCacheEntry` | built | `if (!Settings::UseFileCache())` |
| T34's brief | `:220` | `exists` | built | `return queryCacheEntry(key, [](const FileCache* e) { return std::optio` |
| T35 | `:296` | `statKey` | built | `bool exists = ret == 0;` |
| T35 | `:323` | `insertEntry` | built | `return mFileCache.try_emplace(hash, std::move(fetched)).first->second;` |
| T35 | `:1127` | `exists` | built | `if (enableCache)` |
| T35 | `:1131` | `exists` | built | `return *val;` |
| T35 | `:161` | `fromStat64` | built | `std::unique_lock<std::shared_mutex> guard(mFileCacheMutex);` |
| T35 | `:162` | `fromStat64` | built | `mFileCache[hashPath(key)] = cache;` |
| T33 | `:345` | `FileSystemCache::reset` | built | `FileCache::resetCache();` |
| T33 | `:348` | `FileSystemCache::reset` | built | `void FileSystemCache::reset(const std::string& file)` |
| T33 | `:350` | `FileSystemCache::reset` | built | `FileCache::remove(file);` |
| T33 | `:238` | `isRegularFile` | built | `static std::optional<bool> isRegularFile(const std::string& key)` |
| T26 | `:138` | `fromStat64` | built | `static int fromStat64(const std::string& key, struct stat64* info)` |
| T26 | `:1164` | `isRegularFile` | built | `bool isRegularFile(const std::string& _path)` |

generated, asserted: 17 rows (`tools/t36-tables.py --print filecache`)
<!-- /gen:filecache -->

- **L-19, stage B's lead (`proved: tree`; case 3.26 at stage C).**
  - **Ordering:** `removeFile` erases the path's entry (`:1067`), then asks `isDirectory(_path)` (`:1080`). That stats the still-present file through `queryCacheEntry` and stores `exists = true` (`insertEntry`). Then it unlinks (`:1084`).
  - **Result:** after a successful `removeFile`, `exists(p)` answers `true` from the cache until the next reset. ES's own deleting writer leaves its path stale, so the brief's premise and #1263's (*"ES's own writers drop their entry, so only an outside writer is stale"*) do not hold for `removeFile`. `deleteDirectoryFiles` (`:1512-1531`) inherits it for every file it removes.
  - **Upstream:** ROCKNIX `f6c542872e` and batocera `b2ceb55a7e` have the same order: `FileCache::remove`, then `isDirectory(_path)` twice, then `unlink`, read by `grep -n` over each copy's `removeFile`.
  - **Fix shape (a stream's, not made here):** unlink or `rmdir` first, then erase.
- **#1271's question** (does `isRegularFile` share `exists`'s entry and remember a miss), answered from the source (`proved: tree`; #1271 read at 20:47 UTC with no comments; its body `:38` is the question).
  - **Shared entry: yes.** `FileCache::exists` (`:218-221`) and `FileCache::isRegularFile` (`:238-241`) are two lambdas over one entry found by one hash, and a miss stored by either answers both. The uncached `isRegularFile` (`:1164-1179`) rewrites that shared entry through `fromStat64`.
  - **Symlinks:** a symlinked regular file answers `false` from an entry a listing wrote, because `_symlink` comes from `d_type` there (`:433`, `:575`). It answers `true` from an entry a stat wrote: `stat64` follows the link, so `S_ISLNK` is never true at `:298` or `:152`.
- **T34 L-09** (`HttpReq.cpp:344`, `:479`, through `copyFile`'s erase `:1506-1507`): T34's answer *"sound at the pin"* stands for those two writes. The erase follows the copy, and `copyFile` does not re-read in between.
- **L-12 and the outside writer.** pugixml's `save_file`, `std::ofstream`, `std::rename` outside `renameFile`, libvlc's snapshot, and every other process write without erasing. The stored answer stands until a reset.
  - **The resets** (T33 L-05):
    - `ViewController.cpp:1208` and `:1434`;
    - `FileData.cpp:1113`, after a game exits;
    - `ApiSystem.cpp:496`;
    - `HttpServerThread.cpp:662`;
    - the cache switch `GuiMenu.cpp:1455`.
  - `FileSystemCache::reset(file)` (`:348-351`) has no caller in es-app or es-core at the pin (the grep over both, 6 lines all calling the whole reset).
- **T35's 3.11 and ruling (h) as (a)** (the coordinator's acceptance, comment 6546249036):
  - **At stage C:** T35's case is re-run unchanged from T35's ES and distribution tips of that minute. Both are named with the time of the read and T35's stage (before or after its S6). The record says what the case proves at that tip: the cache's side before S6, the caller's side after.
  - **At the hand-back:** it is re-run once more and named again.
  - **The cache's side, at stage B:** a contained fix for L-19 is certain and goes to the pause. For a write the cache cannot see, the contract stands. `exists(p, false)` at the reads whose writer is outside ES is the guard (`es-code-traps.md:127`, `es-native-ui.md:107`). A stored miss that expires is priced at stage C from 3.13's case, not proposed here.
- **L-15, `preloadFileSystemCache`** (`:1758-1797`):
  - The `[&]` lambda (`:1773`) reads the parameter `trySaveStates` from a detached thread (`:1797`) after the function may have returned (3.6, ASan at stage C).
  - `preloaded` is a function-static `std::set` (`:1766`) read and written with no lock.
  - Its callers are counted at stage C with the case.
- **The five earlier line sets** are the last generated table above: each cited line, the pin's function at it, and whether the image builds that line. T34's brief's `:144` is the WIN32 branch of `fromStat64`, not a line the image runs.

## The texture and font caches

- **#1263's three reads** (`TextureData.cpp:331`, `:339`, `:410`; #1263 read at 20:47 UTC, no comments; `proved: tree`; the cases are 3.13 and 3.26's shapes at stage C, G-03 the frame):
  - **The flow:** `loadFromVideo` (`:322-417`) asks `exists(localFile)` at `:331` with the session cache. When the thumbnail is older than two months it calls `removeFile` (`:336`) and asks again at `:339`.
  - **After the expiry:** with L-19 the second answer is `true`, so the thumbnail is not re-extracted. `:410` answers `true` and `getFileData` reads a file that no longer exists. The texture loads nothing.
  - **On a first extraction:** `:331`'s miss is stored. `createDirectory` at `:341` erases only the parent's entry. libvlc writes the snapshot at `:402` outside `FileSystemUtil`, so `:410` reads the stored miss and returns `false` (`:417`). The thumbnail just made is not used until a reset.
  - **Disposition:** the read is recorded here. The fix is rule 6 at the pause, with an uncached read at `:339` and `:410`, or L-19's order fix, which serves `:339`. #1263 keeps its picture checkbox open for this record (ruling (i)).
- **The texture key's contract** (`TextureResource.cpp:84-165`, T34's inherit item 9):
  - **The key** is `(canonicalPath, tile, linear, shareId)` (`:100`) in a static map of `weak_ptr` with no lock (`:12`, `:146`).
  - **When a key is dropped:** only when its texture has expired and the caller does not ask for a reloadable (`:133-134`), or by the map's own sweep at `:76-81`.
  - **A rewrite on disk** under a living key is never seen. The key carries no file time, and the only reload is `OptimizeVRAM`'s re-size, which reloads the same path synchronously on the caller's thread (`:110-127`, #1221 and T32 PL-07).
  - The caller's half is T34's `02`; #1221's fix is the caller's (`exists(qrPath, false)` and a session-named path).
- **The rest, with their cases (all `pending stage C`):**
  - **L-07:** the font's scale through `getFromTheme`, 3.16.
  - **L-09:** the glyph width, 3.17.
  - **L-10:** `TextureData`'s size fields without `mMutex`, 3.11's TSan line.
  - **L-11:** the loader's `notify_all` and `paused`, 3.12's teardown line.
  - **L-17:** the static caches with no lock. These are the texture map (`TextureResource.cpp:12`), `preloaded` (`FileSystemUtil.cpp:1766`), the battery paths (`Platform.cpp:445-449`) and the font map. 3.25 names the threads that reach each.
- **L-08, a rule erratum against `es-code-traps.md:118`.** The research read `Font::getHeight` as fixed after the constructor (`Font.cpp:107`, `:115-117`, `:420-421`, `:754-757`). The rule says it grows as glyphs rasterise. 3.8 is the positive that decides it at stage C. **T34 PL-17** (*"the moving font height"*, an open item to test) is named beside it for the coordinator's sweep.

## The paths

<!-- gen:paths -->
| Transform | At the pin | Input class | Output | Case |
| --- | --- | --- | --- | --- |
| `getCWDPath` | `:618` | none | the generic cwd, `""` when `getcwd` fails past 2,048 bytes | -- |
| `getPreferredPath` | `:625` | any path | unchanged off WIN32 | -- |
| `getGenericPath` | `:642` | any path | `\` to `/`, `//` folded, trailing `/` dropped | 3.21's inputs |
| `getEscapedPath` | `:670` | a ROM path (the launch's `%ROM%`) | a backslash before each character of the list at `:679` | 3.19 (held at stage B) |
| `getCanonicalPath` | `:707` | any path | the `.`/`..` fold | 3.20 (held at stage B) |
| `getAbsolutePath` | `:787` | a relative path and a base | `getCanonicalPath(base + "/" + path)` unless absolute | -- |
| `getParent` | `:795` | any path | the text before the last `/` | -- |
| `getFileName` | `:804` | any path | the text after the last `/` | -- |
| `getStem` | `:813` | any path | the file name less its last extension | -- |
| `getExtension` | `:842` | any path | from the last `.` of the file name | -- |
| `changeExtension` | `:859` | a path and an extension | the extension replaced | -- |
| `resolveRelativePath` | `:890` | a path and a root | `./` and `~/` resolved against the root | -- |
| `createRelativePath` | `:917` | a path and a root | `./`-relative by string prefix | 3.21 (`.//a.png`) |
| `removeCommonPath` | `:980` | a path and a prefix | the rest by string prefix, not by component | 3.21 |
| `resolveSymlink` | `:999` | a path | `readlink`'s target, made absolute | -- |
| `combine` | `:1261` | a base and a name | joined; a leading `/..` climbs the base | -- |
| `megaBytesToString` | `:1533` | a size | a display string | -- |
| `kiloBytesToString` | `:1554` | a size | a display string | -- |
| `getTempPath` | `:1575` | none | the temp folder, created | -- |
| `getPdfTempPath` | `:1599` | none | the PDF temp folder, emptied | -- |
| `getFileCrc32` | `:1623` | a file | hex CRC32 | -- |
| `getFileMd5` | `:1664` | a file | hex MD5 | -- |

generated, asserted: 22 rows (`tools/t36-tables.py --print paths`)
<!-- /gen:paths -->

- **`getEscapedPath`'s list** (`:679`, 19 characters, the launch's `%ROM%`): read whole. What it leaves, and what that reaches, is held under D-WORKFLOW-215 (§ The leads). 3.19 runs at stage C into the held directory.
- **`getCanonicalPath`:** the brief's 3.20 (R4 item 16, T2's lead). Its callers were read whole at stage B under ruling (k), and the result is held.
- **`createRelativePath` and `removeCommonPath`** (`:917-997`) compare by string prefix: `/storage/roms/snes2/a.png` against `/storage/roms/snes` gives `.//a.png` (R4 item 17, 3.21, `pending stage C`).
- **`isAbsolute`** is `path[0] == '/'` off WIN32 (`:1149-1162`, T2 FD-14, cited).
- **`CommandLineUtil.h`'s `wordEnd`:** T1's F-07 (#730), cited.

## The processes

<!-- gen:processes -->
| Line | Function | Match | Image | Shell | Waits | Returns | Callers' thread |
| --- | --- | --- | --- | --- | --- | --- | --- |
| `Platform.cpp:167` | `run` | spawn | built | `system()` (`/bin/sh -c`) when waiting; `execl("/bin/sh")` in a grandchild when not | when `waitForExit` (the launch, `main.cpp:540`, `InputManager.cpp:1272`, `Scripting.cpp:133`, `:142`); not at `Scripting.cpp:45` | `WEXITSTATUS` of the wrap's `exit $xs` (L-05); `0` when not waiting, or when the first `fork` fails | the launch on the interface thread (`FileData.cpp:1100-1103`) |
| `Platform.cpp:172` | `run` | spawn | built | `system()` (`/bin/sh -c`) when waiting; `execl("/bin/sh")` in a grandchild when not | when `waitForExit` (the launch, `main.cpp:540`, `InputManager.cpp:1272`, `Scripting.cpp:133`, `:142`); not at `Scripting.cpp:45` | `WEXITSTATUS` of the wrap's `exit $xs` (L-05); `0` when not waiting, or when the first `fork` fails | the launch on the interface thread (`FileData.cpp:1100-1103`) |
| `Platform.cpp:175` | `run` | spawn | built | `system()` (`/bin/sh -c`) when waiting; `execl("/bin/sh")` in a grandchild when not | when `waitForExit` (the launch, `main.cpp:540`, `InputManager.cpp:1272`, `Scripting.cpp:133`, `:142`); not at `Scripting.cpp:45` | `WEXITSTATUS` of the wrap's `exit $xs` (L-05); `0` when not waiting, or when the first `fork` fails | the launch on the interface thread (`FileData.cpp:1100-1103`) |
| `Platform.cpp:178` | `run` | spawn | built | `system()` (`/bin/sh -c`) when waiting; `execl("/bin/sh")` in a grandchild when not | when `waitForExit` (the launch, `main.cpp:540`, `InputManager.cpp:1272`, `Scripting.cpp:133`, `:142`); not at `Scripting.cpp:45` | `WEXITSTATUS` of the wrap's `exit $xs` (L-05); `0` when not waiting, or when the first `fork` fails | the launch on the interface thread (`FileData.cpp:1100-1103`) |
| `Platform.cpp:179` | `run` | comment | built | -- | -- | -- | -- |
| `Platform.cpp:199` | `runShutdownCommand` | spawn | WIN32 only | `system()` | yes | `system()`'s raw status, not `WEXITSTATUS` | the quit path |
| `Platform.cpp:201` | `runShutdownCommand` | spawn | built | `system()` | yes | `system()`'s raw status, not `WEXITSTATUS` | the quit path |
| `Platform.cpp:208` | `runRestartCommand` | spawn | WIN32 only | `system()` | yes | `system()`'s raw status, not `WEXITSTATUS` | the quit path |
| `Platform.cpp:210` | `runRestartCommand` | spawn | built | `system()` | yes | `system()`'s raw status, not `WEXITSTATUS` | the quit path |
| `Platform.cpp:248` | `touch` | comment | built | -- | -- | -- | -- |
| `Platform.cpp:858` | `runSystemCommand` | spawn | built | `execl("/usr/bin/sh")` in a grandchild | **yes**: the child waits for the grandchild and the caller waits for the child (L-13) | `0` always (`:879`) | the interface thread for most of its 80 call lines (#1220) |
| `Platform.cpp:861` | `runSystemCommand` | spawn | built | `execl("/usr/bin/sh")` in a grandchild | **yes**: the child waits for the grandchild and the caller waits for the child (L-13) | `0` always (`:879`) | the interface thread for most of its 80 call lines (#1220) |
| `Platform.cpp:864` | `runSystemCommand` | spawn | built | `execl("/usr/bin/sh")` in a grandchild | **yes**: the child waits for the grandchild and the caller waits for the child (L-13) | `0` always (`:879`) | the interface thread for most of its 80 call lines (#1220) |
| `Platform.cpp:865` | `runSystemCommand` | comment | built | -- | -- | -- | -- |
| `Platform.cpp:894` | `GetShOutput` | spawn | built | `popen()` (`/bin/sh -c`) | yes (to EOF, `pclose`) | each `fgets` chunk loses its last byte: the newline of a short line, a real character past 255 bytes or at an unterminated end (L-06); `popen` failure unchecked | its 27 call lines' (T26's collision) |
| `Platform.cpp:911` | `GetShOutputLines` | spawn | built | `popen()` | yes | the lines; `popen` failure returns none | its 9 call lines' |

generated, asserted: 16 rows (`tools/t36-tables.py --print processes`)
<!-- /gen:processes -->

The 16 lines are 13 spawns and 3 comment matches (`:179` and `:865` are `// execl failed`; `:248` is the commented `system("touch ...")` in `touch`, built). 11 of the 13 are built into the image; `:199` and `:208` are WIN32 only.

- **L-05, `run()`'s wrap** (`Platform.cpp:162-168`):
  - **The host's rcs:** the literal printed `seq 400 rc=0` and `seq 200000 rc=141` under the host's `/usr/bin/dash` at stage A (`stage-a/runs.out`, `proved: tool-run`).
  - **The launch's disposition (the errata's):** the launch does not run with SIGPIPE's default. `httplib::Server` ignores it and every child inherits that, so past the pipe's buffer the launch gets EPIPE and lost output, not a signal.
  - **G-07 at the window:** it first reads `SigIgn` (bit `0x1000`) of the running EmulationStation, then the image's shell rcs and the image's `runemu.sh`.
  - **The wrapper's redirects** from the distribution at `a5fbd75d61` (`runemu.sh` last changed `6f2eb9c212`, 2026-10-14):
    - `:40` `LOG_FILE="exec.log"`;
    - `:46` `OUTPUT_LOG="${LOG_DIRECTORY}/${LOG_FILE}"`;
    - `:84` `... 2>&1 | tee -a ${LOG_DIRECTORY}/${LOG_FILE}`;
    - `:491` `"${ROMNAME}" &>>${OUTPUT_LOG}`;
    - `:500` `eval ${RUNTHIS} &>>${OUTPUT_LOG}`.
  - **What reaches the pipe:** the emulator's output is appended to the log and does not reach `run()`'s pipe; the wrapper's `tee`'d lines do. That ES's launch command is this script stays `[unverified]` until the guest.
- **L-13, a rule erratum against `es-native-ui.md:103`.** The rule calls `runSystemCommand` the way to run an OS command without blocking.
  - At the pin it returns `0` at `:879`, reads neither `name` nor `window`, and blocks: the child waits for the grandchild (`:867-868`) and the caller waits for the child (`:876`). It is a double fork that does not detach.
  - 3.7's text case records it (`pending stage C`). #1220 (process starts on the interface thread) is its callers'.
- **L-06, `GetShOutput`** (`:891-905`): T26's collision (#1225, `a5d2d3756` on `757f5370ea`). 3.9 is the FAIL-at-pin control at stage C, never re-fixed here.
- **`shellQuote`** (`StringUtil.cpp:426-444`) is the contract four lanes' fixes rest on: single quotes, `'` as `'\''`, the empty string as `''`. 3.18's positive is at stage C.
- **L-14, `maskSecrets`' reach** (`StringUtil.cpp:446-804`). 18 call lines over es-app and es-core (`grep -c 'maskSecrets('`), in 10 files, the definition among them. `runSystemCommand` logs every command through it (`Platform.cpp:855`), and the launch logs its command through it (`FileData.cpp:1090`). 3.10's JSON, `name: value` and `Authorization: Bearer` shapes, each built at run time, run at stage C.

## The writes and reads

<!-- gen:writes -->
| Site | Function | Image | Mechanism | Atomic | What an interrupted write leaves | What its return claims |
| --- | --- | --- | --- | --- | --- | --- |
| `FileSystemUtil.cpp:1053` | `removeDirectory` | WIN32 only | `rmdir` | atomic | nothing (the directory stays) | true when `rmdir` returned 0; true when absent |
| `FileSystemUtil.cpp:1055` | `removeDirectory` | built | `rmdir` | atomic | nothing (the directory stays) | true when `rmdir` returned 0; true when absent |
| `FileSystemUtil.cpp:1070` | `removeFile` | WIN32 only | `unlink` / `rmdir` | atomic | nothing | true when it returned 0; true when absent; the path left cached as present (L-19) |
| `FileSystemUtil.cpp:1072` | `removeFile` | WIN32 only | `unlink` / `rmdir` | atomic | nothing | true when it returned 0; true when absent; the path left cached as present (L-19) |
| `FileSystemUtil.cpp:1075` | `removeFile` | WIN32 only | `unlink` / `rmdir` | atomic | nothing | true when it returned 0; true when absent; the path left cached as present (L-19) |
| `FileSystemUtil.cpp:1081` | `removeFile` | built | `unlink` / `rmdir` | atomic | nothing | true when it returned 0; true when absent; the path left cached as present (L-19) |
| `FileSystemUtil.cpp:1084` | `removeFile` | built | `unlink` / `rmdir` | atomic | nothing | true when it returned 0; true when absent; the path left cached as present (L-19) |
| `FileSystemUtil.cpp:1100` | `createDirectory` | WIN32 only | `mkdir 0755`, parents by recursion | per directory | the parents made so far | false on a race with another creator (L-16) |
| `FileSystemUtil.cpp:1105` | `createDirectory` | built | `mkdir 0755`, parents by recursion | per directory | the parents made so far | false on a race with another creator (L-16) |
| `FileSystemUtil.cpp:1116` | `createDirectory` | built | `mkdir 0755`, parents by recursion | per directory | the parents made so far | false on a race with another creator (L-16) |
| `FileSystemUtil.cpp:1432` | `writeAllText` | WIN32 only | `fopen "wb"` in place, `fwrite`, `fclose` | **no**: truncate then write | a truncated or short file | nothing: `void` (L-04, #1186) |
| `FileSystemUtil.cpp:1434` | `writeAllText` | built | `fopen "wb"` in place, `fwrite`, `fclose` | **no**: truncate then write | a truncated or short file | nothing: `void` (L-04, #1186) |
| `FileSystemUtil.cpp:1461` | `renameFile` | WIN32 only | `std::rename` | atomic on one filesystem | src or dst | true over an absent source (L-03; T21's fix) |
| `FileSystemUtil.cpp:1463` | `renameFile` | built | `std::rename` | atomic on one filesystem | src or dst | true over an absent source (L-03; T21's fix) |
| `FileSystemUtil.cpp:1490` | `copyFile` | WIN32 only | `fopen "wb"` in place, 512-byte `fread`/`fwrite` | **no** | a short destination | true over an absent source and over a short write (L-03) |
| `FileSystemUtil.cpp:1492` | `copyFile` | built | `fopen "wb"` in place, 512-byte `fread`/`fwrite` | **no** | a short destination | true over an absent source and over a short write (L-03) |
| `Platform.cpp:244` | `touch` | built | `open` with `O_CREAT` and `O_WRONLY`, mode `0644`, no truncation | yes (creates or leaves) | an empty file or the old one | nothing: `void` |
| `ZipFile.cpp:259` | `ZipFile::extract` | built | miniz `MZ_FOPEN(..., "wb")` (`zip_file.hpp:6634`) | **no** | a partial member | miniz's status |

generated, asserted: 18 rows (`tools/t36-tables.py --print writes`)
<!-- /gen:writes -->

- **L-04 and #1186:** `writeAllText` (`:1429-1446`) truncates in place, ignores `fwrite` and `fclose`, and returns `void`. #1186's last comment as read is 6440869119 (2026-10-27 11:33 UTC). Whether the function returns its result or is marked as superseded by `AtomicFile::writeText` is put to the pause; the call sites stay their owners' under #1186.
- **L-03** (`proved: tree`, case 3.2 at stage C):
  - `renameFile` returns `true` over an absent source (`:1451-1452`), and with `overWrite` removes the destination before renaming (`:1454-1455`). Both are T21's fix (#1191, `f7c16144d`), a collision.
  - `copyFile` returns `true` over an absent source (`:1472-1474`) and over a short write: `fwrite`'s count is unread (`:1500-1501`) and so is `fclose`'s (`:1503`). That half is this slice's (rule 6).
- **L-02:** `skipUtf8Bom` (`:1369-1379`) leaves the stream failed for a file under three bytes, so `readAllText` (`:1418-1427`) and `readAllLines` (`:1400-1416`) read nothing. T20's collision (#1177, `d9afa5c7c`); 3.4 is the control.
- **L-16:** `createDirectory` (`:1089-1120`) returns `false` when another creator made the directory between its `exists` and its `mkdir` (3.15).
- **`readAllBytes`** (`:1381-1398`) returns empty on a short read and for a file whose size `tellg` cannot give; no lead.

## The device reads, the renderers and the words

- **The case helpers:** `toUpper` and `toLower` (`StringUtil.cpp:357-362`, `:398-403`), L-01, 3.1.
- **The battery read, for #840** (`Platform.cpp:440-560`, `proved: tree`):
  - The paths are found once, by a listing of `/sys/class/power_supply` through the cached `getDirContent` (`:458`), and kept in five function-static strings with no lock (`:445-449`).
  - The capacity is read uncached each call: a fresh `std::ifstream` (`:546-557`), the status through `readAllText` (`:524`).
  - The fuel-gauge branch's `std::stof` (`:539-540`) throws on an empty read.
  - So #840's question has no cache in the read itself. A supply added after the first call is never found.
- **`TimeText`:** the fork's file, read whole (`TimeText.cpp`, 83 lines); its cases are T18's in `es-unit-tests`.
- **The 11 `_("` lines** (stage A's count: 11 lines, 12 occurrences), with the French from the pin's catalog (`locale/lang/fr/LC_MESSAGES/emulationstation2.po`, parsed at stage B):

  | Line | msgid | French |
  | --- | --- | --- |
  | `MathExpr.cpp:95` | `Unknown`, `None` | `Inconnu`, `Aucun` |
  | `TimeUtil.cpp:517`, `:588` | `never` | `jamais` |
  | `TimeUtil.cpp:544` | `%d d` | `%d j` |
  | `TimeUtil.cpp:548`, `:569` | `%d h` | `%d h` |
  | `TimeUtil.cpp:552`, `:560`, `:573`, `:578` | `%d mn` | `%d mn` |
  | `TimeUtil.cpp:580` | `%d sec` | `%d sec` |

  `es-untranslated` printed 706 of 706 fork strings with French (stage A). G-04 draws the durations at 640x480 in both languages (`pending window`).
- **The renderers:**
  - The image builds `Renderer_GLES30.cpp` (`-DGLES3=1` on every device, R3 § 2.2). The guest runs it through Mesa virgl; H700 runs panfrost and SM8550 Adreno, which the guest cannot show (G-09 `CANNOT`).
  - The GL thread question is 3.25's and G-05's.

## The structure

- **Three renderers no image compiles:** `Renderer_GL21`, `Renderer_GLES10` and `Renderer_GLES20` (G-08 `CANNOT`, a structure fact).
- **Includes:** the angle includes outside the lane's standard list are 33 of 241 (`stage-a/angle-includes.out`); R3's 41 was against an unstated list. The branches the host did not parse, and the stand-in's renderer positives, are stage C's (`stage-a/syntax-check.out` owed).
- **`ROCKNIX` gates in the 58: 0.** The one mention is a comment (`CommandLineUtil.h:51`).
- **`han.h` (20,923 lines) and `zip_file.hpp` (10,011 lines):** read only where a lead reaches them. `zip_file.hpp`'s provenance and licence notice belong to #256's vendored-header PR bucket.
- **T21's `utils/DownloadFile.{h,cpp}`** fall under the glob and are not at the pin (ruling (b)).
- **The fakes' double:** stage C's.
- **The two rule errata, for the coordinator's sweep:**
  - **L-08** against `es-code-traps.md:118`, with 3.8's PASS line;
  - **L-13** against `es-native-ui.md:103`, with 3.7's text case.
- **The menu map's checker:** `55 screen(s) at 16dbac521, 31 in the map, 24 declared unmapped, 0 missing` (stage A).

## The merge debt

- **The bases:** `cada856d86` is the base against ROCKNIX's master `f6c542872e`, and `bccd715707` is its parent.
- **Upstream:** upstream commits on the 58: 0 (14 on any path). 43 of 58 blobs are identical pin to master. Batocera has 13 commits since `1750dded8c` on nine files, four of them fork-modified; that is the reconciliation list only.
- **The pending collisions:**
  - T20's `d9afa5c7c` (`FileSystemUtil.cpp`, `readAllText`, #1177) on `5c0ddaaeef`;
  - T21's `f7c16144d` (`FileSystemUtil.cpp`, `renameFile`, #1191) on `3ae9610b0f`;
  - T26's `a5d2d3756` (`Platform.cpp`, `GetShOutput`, #1225) on `757f5370ea`;
  - T21's two new files, `utils/DownloadFile.{cpp,h}`, under the glob.
  - Each is read and recorded in `stage-a/collisions.out`, and never re-made here.

## The runs

- **Stage A:** 23 runs, each as the brief expected (`stage-a/runs.out`, `00`).
- **Stage C:** `pending stage C`. The `utils-resources-tests` build, the cases 3.1 to 3.26, T35's 3.11 re-run under ruling (h) as (a), and the stand-in over the 25 `.cpp` files.

## The guest cycle

`pending window`. The plan is `stage-b/window-plan.md`, asked for on #683 at stage B with its bound.

## The streams

## Positives

- **The cache's lock discipline:** `queryCacheEntry` stats outside the lock and `insertEntry` re-checks under the unique lock, so two threads that miss together store one answer (`:200-216`, `:313-324`; `proved: tree`, 3.25's TSan program at stage C).
- **`GetShOutputLines`** (`Platform.cpp:907-935`) accumulates a line longer than its buffer and checks `popen`, which `GetShOutput` does not.
- **`writeAllText`, `renameFile` and `copyFile`** erase after they write. Only `removeFile` re-reads in between (L-19).
- **The battery's capacity read** is uncached.

## The #585 lines owed

- **The three never posted (D-WORKFLOW-165), for the coordinator:**
  - T20 `02:337`, `skipUtf8Bom` (batocera);
  - #1191 `:21`, `renameFile`;
  - T26 `02:819`, `GetShOutput` (ROCKNIX's alone).
- **This slice's, so far:**
  - L-19, `removeFile`'s order (ROCKNIX and batocera both). It is written in the shape the lane writes at stage D and never sent.
  - The three holds' lines are held with their records.

## What T37 inherits

Written at the hand-back. Its tables are the five above, the provenance table and the lines-set reconciliation. The `utils-resources-tests` recipe, the stand-in's rc per file, the rule errata as dispositioned and the collision list follow at stages C to E.


## The brief's § 4, the questions

## 4. The questions

Each answered in `04-analysis.md` with the evidence at its lines; a defect
proved becomes a `bug` with its trace, its `Already written:` line and its
VM line (D-WORKFLOW-187), in one of the families the earlier ES briefs
used -- **a layout computed from what it last produced or from a moving
number**, **a house constant a surface does not keep**, **a prompt offered
where the key moves nothing**, **a lifetime or a thread**, **a read of a
file another process writes**, **a player sentence outside the vocabulary
or without its French**, **a structure or merge-debt fact** -- with the
lens, cost against value, asked of every upstream surface: what it costs
the player (a frame's work, a wait, a thread) against what it gives. The
leads are § 2's L-01 to L-18, cited here by number (their lines are the
table's and are not restated), and the floor's pure leads tabled at the end
of this section; each is read at its lines before it is called anything,
and the candidates marked FAIL-at-pin (§ 5) get their `git log -S` first
(`engineering-practices.md` § Verify design intent); the upstream surfaces
outside the lanes are § 1's list, read and recorded, fixed only under rule 6
(D-UI-079). For this slice the natural homes (R3 § 4): the `exists` cache is
*a read of a file another process writes*; `Font::getHeight` and the double
`fontScale` are *a layout computed from a moving number* (and L-08 asks
whether the number moves at all); `FileCache`'s `shared_mutex`, the texture
loader's teardown, `TextureData`'s unlocked fields, `ThreadPool` and
`StringListLock` are *a lifetime or a thread*; the 11 `_("` lines and the
case helpers are *a player sentence*; the three renderers no image compiles
and T21's `DownloadFile.*` under the glob are *a structure fact*. The seven
questions are R4 § 1's proposal, in T35's shape (Q1 to Q6 by subject, Q7
the lens's).

- **Q1 The file cache: what `exists` answers, who erases, who resets**
  (`es-code-traps.md:127`; `es-native-ui.md:107`; the reads and the
  threads runs). **L-12**: the cache's contract stated from the source --
  a miss stored (`:213-215`), a listing's wildcard answering "absent"
  without a stat (`:277-282`), `exists(p, false)` rewriting the entry
  (`:161-162`), the six erasing writers (`:1051`, `:1067`, `:1097`, `:1445`,
  `:1457-1458`, `:1506-1507`), the one reset (`:343-346`), and **every
  writer outside this file** (pugixml `save_file`, `std::ofstream`,
  `std::rename`, another process) invisible to it; **one reconciled table**
  over the five line sets the earlier lanes cited (the take-up table's
  items 6-11), each set mapped onto the pin's lines; **#1271's question**
  (does `isRegularFile` share the entry and remember a miss) answered from
  the source; **T34 L-09's answer** (*"sound at the pin"*) cited for
  `HttpReq`'s writes. **Ruling (h)**: T35's 3.11 FAILs at the pin in T35's
  harness; this slice decides the cache's side -- whether a contained fix
  (an erase on every writer this file cannot see is impossible; a stored
  miss that expires, or a miss never stored, is the shape to price) is put
  to the pause, or the contract stands and the rules' sentences
  (`es-code-traps.md:127`, `es-native-ui.md:107`) are the guard -- and
  states which in `02` § The file cache; T35's case is re-run unchanged
  only by a stage-E stream (§ 5 item 4). **L-15**: `preloadFileSystemCache`'s
  `[&]` lambda reading `trySaveStates` on a detached thread after its
  function returned (3.6, the ASan stand-in) and its unlocked static
  `preloaded`; its callers counted by the lane. A table: every cache entry
  point (`queryCacheEntry`, `insertEntry`, `getCacheEntry`, `remove`,
  `reset`, `fromStat64`), its lock (shared or exclusive), its callers'
  count, and the answer it gives a file another process wrote.
- **Q2 The texture and font caches** (`es-code-traps.md:104`, `:109`,
  `:118`; D-UI-050; #1263; the threads, writes and includes runs).
  **#1263's cache half** (ruling (i)): the three cached
  `exists(localFile)` at `TextureData.cpp:331`, `:339`, `:410` against a
  picture rewritten from outside under the same path; **the texture-cache
  contract** (T34's inherit item 9): `TextureResource::get`'s key
  (`:100`), when a key is dropped (the `weak_ptr` map `:12`, `:146`), and
  whether a rewrite on disk is ever seen while a texture lives under the
  key; the synchronous reload on the caller's thread (`:110-127`), priced.
  **L-10**: the fork's #181 bookkeeping (`setMaxSize`, `rasterizeAt`)
  without `mMutex` beside a loader writing the same fields under it (3.11's
  TSan stand-in), and batocera's `9c48a461b` / `0f9242aee` on the same file
  read as the reconciliation's other side (§ 2). **L-11**: the loader's
  teardown -- `notify_all` without the lock, `paused` keeping every loader
  asleep and the join waiting (3.12). **The font**: **L-07** `getFromTheme`'s
  double scale (3.16; whether the shipped theme reaches it, from the theme's
  XML on the guest, G-01); **L-08** **the rule erratum**: the constructor
  rasterises ASCII 32..127 (`Font.cpp:115-117`, 2014), so `getHeight()` is
  fixed after construction, against `es-code-traps.md:118` and T34's L-02 /
  PL-17 -- 3.8's positive is the proof, the rule sentence is **the
  coordinator's sweep** (`tools/archaeology --reversal 'tallest glyph'`),
  never the lane's edit, and whether PL-17's open item closes on it is the
  pause's; **L-09** measure against draw for a substituted glyph and the
  newline advance (3.17); **L-17** which threads call `Font::get`,
  `sizeText` or `TextureResource::get` -- a question before a claim; a
  worker that measures text reaches `getGlyph`'s GL upload off the context
  thread. A table: every cache in `resources/` (the font map, the
  substitutable characters, the glyph maps, the texture map, the data
  manager's MRU), its key, its lock or none, its eviction, and its readers'
  threads.
- **Q3 Paths and escaping** (the take-up table's items 15 to 19; no R2 lead
  -- R2 did not open these functions). **`getEscapedPath`'s character
  list** (`%ROM%` alone goes through it after T2's fix; T2's second opinion
  *"cannot certify universal `%ROM%` safety"*): what the list leaves, with
  3.19 over the shell's metacharacters, and **rule 6** if it leaves one a
  ROM name can carry; **`getCanonicalPath`'s fold** (32 component indexes,
  the count unchecked, `:726` by T2's line): 3.20, **rule 6** if it writes
  past the array; **the relative path by prefix** (`.//a.png`, `:986`):
  3.21, a disposition (none found); `isAbsolute` and `CommandLineUtil`'s
  `wordEnd` cited (T2's, T1's sides). A table: every path transform in
  `FileSystemUtil` with its input class, its output, and the case that
  holds it.
- **Q4 Processes and the shell: what `run()`, `runSystemCommand` and
  `GetShOutput` promise** (`handheld-evidence.md`; #1220; ruling (j); the
  spawns run). **L-05**: `run()`'s wrap -- `head -300` of stdout, and
  SIGPIPE with status 141 **only once the command's output outruns the pipe
  buffer** (a 400-line output, 1,492 bytes, is held whole and exits 0; 200,000
  lines printed 141, proof C1, CMD4, CMD12); the log path unquoted; `2>`
  binding only the last simple command; both logs overwritten -- with **the
  literal's two host-shell runs at stage A** (3.5) and the image's busybox
  shell on the guest (G-07); **the launch wrapper's redirects read from the
  source** (`runemu.sh:491`, `:500` append the emulator's output to its log;
  `:84` `tee`s the wrapper's own log lines to stdout, so those reach the
  pipe, proof C15) and the image's copy confirmed in G-07; that ES's launch
  command is this script is the lane's trace (proof C15: not settled); the
  callers with `waitForExit` true named. **L-13**: `runSystemCommand` returns 0 always,
  blocks its caller for the command's whole run, and ignores `name` and
  `window` -- 78 call sites, none reading the return; **the rule erratum**:
  `es-native-ui.md:103` says passing `window` shows a splash, and nothing
  does at the pin (3.7's text case and the body's lines are the proof,
  `proved: tree`); the rule sentence is **the coordinator's sweep**, not
  the lane's edit. **L-06**: `GetShOutput`'s lost byte and unchecked
  `popen` -- **T26's fix, a collision** (ruling (d)); this slice's 3.9 is
  the control and the joined-lines contract for upstream's callers is
  stated. **`shellQuote`** (3.18): the contract four lanes' fixes rest on.
  **L-14**: `maskSecrets`'s reach -- the `=`-only test leaves `name:
  value`, JSON and `Authorization:` unmasked (3.10); whether any logged
  line carries those shapes is the lane's grep over the call sites, never
  a claim from the name. **L-18**: the quit path's leaked event, recorded.
  A table: every spawn in the 58 (the 16 lines, all `Platform.cpp`), the
  shell it runs (`/bin/sh` in `run`, `/usr/bin/sh` in `runSystemCommand`),
  whether it waits, what it returns, and which thread its callers run on.
- **Q5 Writes and reads: the helpers' false successes**
  (`upgrade-and-install.md`; D-CLOUD-078; the writes run). **L-03**
  (**FAIL at the pin**, 3.2): `renameFile` and `copyFile` return `true`
  over an absent source, `copyFile` over a short write, `renameFile`'s
  destination removed before an atomic rename and `overWrite = false`
  unprotected on POSIX -- **`renameFile`'s half is T21's fix, a collision**
  (ruling (d)); **`copyFile`'s is this slice's**, with the callers that
  branch on the return (`HttpReq.cpp:479-506`, `Scraper.cpp:672`,
  `SaveState.cpp:154-155`, `GuiMetaDataEd.cpp:483`, `Win32ApiSystem.cpp:745`,
  `:877`) named for their owners. **L-04** (3.3): `writeAllText` cannot
  report a failure -- **T21 PL-20 / Backlog #1186**, whose ruling moves the
  call sites, not the function; **the pause** asks whether the function
  returns its result or is marked superseded by `AtomicFile::writeText`;
  the cloud stamp's temp-and-rename that publishes a short write
  (`ThreadedCloudSync.cpp:943-948`, T18's) named for its owner. **L-02**
  (3.4): the under-three-bytes read -- **T20's fix, a collision**; this
  slice's case is the control. **L-16** (3.15): `createDirectory`'s
  `false` for a directory a concurrent creator made. **No write in the 58
  is temp-and-rename** (R2 § 5): the tree's atomic writer is T21's. A
  table: every write site (the corrected pattern's `:1432`, `:1434`,
  `:1490`, `:1492`, the `rmdir`, `unlink`, `mkdir` and `std::rename` lines,
  `Platform.cpp:244`'s `open(O_CREAT|O_WRONLY)`), its mechanism, whether
  it is atomic, what an interrupted write leaves, and what its return
  claims.
- **Q6 Device reads, the renderers and the fork's text** (`es-player-text.md`
  § Conventions; D-WORKFLOW-144; #840; the strings, includes and non-ASCII
  runs). **L-01** (**FAIL at the pin**, 3.1): `toUpper`/`toLower` corrupt a
  3-byte character with a case pair (Vietnamese, full-width Latin), French
  2-byte accents unaffected; the brand's formatter is a component's (ruling
  (f)); **rule 6** if the fix is contained (`=` for `+=` in the two 3-byte
  branches), the different-length pairs read. **The fork's text**:
  `TimeText` and `TimeUtil`'s fork hunk (the save state manager's times,
  D-UI-058, D-UI-087, D-UI-089), whole; the 11 upstream `_("` lines and
  their French (the catalog parse, § 5; G-04's frames at 640x480 in both
  languages). **#840**: the battery read in `Platform.cpp` that T35's
  watcher polls -- the capacity read and any cache in it, for #840's VM
  checkbox. **The renderers** (no routed item names one, R4 § 1): the
  image builds `Renderer_GLES30.cpp` alone (`-DGLES3=1` ->
  `USE_OPENGLES_30`), **no lane's stand-in has parsed `Renderer.h`'s
  GLES30 branches**, and no thread check exists anywhere in `renderers/`
  (L-17's GL half); the guest runs the same source through Mesa virgl
  (G-05) and **cannot show panfrost's (H700) or Adreno's (SM8550)** -- a
  driver-specific renderer defect is an `open item to test`
  (`bugs-are-agent-first.md`), and the physical fact is the device's
  (`vm-first.md`).
- **Q7 Cost against value, the structure and the merge debt**
  (`time-to-play.md`; `engineering-practices.md` § Change stays inside the
  fork's lanes, § Check upstream early; D-UI-079, D-WORKFLOW-162; the
  membership, scope, delta, includes and non-ASCII runs). **The lens, asked
  of every upstream surface in § 1's list**: `han.h` (20,923) and
  `zip_file.hpp` (10,011) are 30,934 of the 50,840 lines (R1 C09) -- **a
  reading-scope decision, not a figure error** (R1 § 6 D5): what each
  costs the binary and the reader against what it gives (the Korean input
  table; the backup archives' reader, #256's *"its own PR"*), read by
  cited range and recorded; the thread pool's sizing
  (`hardware_concurrency() * mThreadByCore`, `ThreadPool.cpp:26`); the
  texture loader's thread count (`:215-223`); the VRAM budget's tiers (T21's
  `Settings.cpp:233-246`); **the three renderer pairs no image compiles a
  body of** (`Renderer_GL21`, `Renderer_GLES10`, `Renderer_GLES20`: in the
  unconditional CMake list, empty under the image's defines -- a structure
  fact, R3 § 2.2, § 4); `fribidi`'s branch (`HAVE_FRIBIDI`, **whether the
  image build takes it is `[unverified]`**: ES's `CMakeLists.txt:236-241` defines it when `pkg_check_modules(FRIBIDI QUIET fribidi)` finds the library, `package.mk` names no fribidi, `vlc` is built `--disable-fribidi` (`vlc/package.mk:98`), and the tree's `packages/devel/fribidi` is a dependency of `pango` (`pango/package.mk:11`), so whether it is in the sysroot when ES configures is build order, not source (proof U-1, CMD4, CMD8, CMD12, CMD13) -- G-01's `ldd`
  settles it, `image` side); `vlc/vlc.h` unguarded in `TextureData.cpp:12`; **0
  `#if...ROCKNIX` lines in the 58** (R3 cmd 17); the include reach (241
  angle-include lines, proof CMD4, of which 41 non-standard by R3's rule
  with its standard list unstated; 0 quoted external, one macro include, R3 cmd
  9). **The structure**: the 43 identical to `rocknix/master`; T21's
  `utils/DownloadFile.*` falling under the glob at T21's tip (ruling (b));
  the three lane fixes in two of the 58 (ruling (d)); the fakes' double
  (ruling (g)). **Merge debt: none** on the 58 (§ 2's one line);
  **batocera's thirteen** since `1750dded8c` on nine files, four of them
  fork-modified (`Font.cpp`, `Font.h`, `TextureData.cpp`, `Platform.cpp`),
  as the reconciliation list -- the SVG size pair against the fork's #181,
  the fribidi pair against the tab stops, the battery fallback; the hunk
  ranges the lane's `git diff 1750dded8c batocera/master -- <file>` per
  file, never a merge; #791's Q4 list appended by the coordinator from the
  lane's `02`. **The #585 lines owed** (R4 § 5): the three never posted
  (T20's `skipUtf8Bom` for batocera, #1191's `renameFile`, T26's
  `GetShOutput` for ROCKNIX) and this slice's for each upstream-carried
  defect it closes under rule 6 (the case helpers, `copyFile`,
  `preloadFileSystemCache`, the loader's teardown, `getFromTheme`) -- each
  a line the lane writes in `02` for the coordinator to post, never sent
  (D-WORKFLOW-164/165). **The map**: no row of this slice's own; the
  checker reads no slice file (§ 3 item 3).

### The floor's pure leads, carried

The research ran no case (R3 header: *"Nothing was built, compiled or run
against the pin"*), so every row is a candidate until the lane's stage C;
the seams are in the shape `file:line at the pin | the function | what a
case would catch`, each a case in `CloudText`'s shape (`es-code-traps.md` §
Pure text has a home, and a test; § 5 item 1) built by the slice's binary --
**already linked whole** in `es-unit-tests` (`StringUtil.cpp`, `TimeText.cpp`,
`OfflineProxyUrl.cpp`), **linkable whole with test-defined doubles** in T20's
and T21's shape (`FileSystemUtil.cpp` with `StringUtil.cpp` and `md5.cpp`;
`TimeUtil.cpp`, `HtmlColor.cpp`, `md5.cpp`, `Randomizer.cpp`,
`StringListLock.cpp`, `ResourceManager.cpp`, `ThreadPool.cpp` with the
`Platform` functions doubled), or an **extract** (the function's text lifted
into the case, T35's `t35-extract.py` SPECS shape, refusing on drift) where
the source is parse-only (`Platform.cpp`'s `GetShOutput`, `Font.cpp`'s
scaling, `TextureDataManager::cleanupVRAM`, `FileSystemUtil`'s
`FileCache`/`exists`) (R3 § 3). **The candidates the drafter marks
FAIL-at-pin are in bold; the coordinator's order puts L-01, L-03/L-04,
L-05, L-15, L-13 and L-08 first.** A case for a credential shape (3.10)
builds its value at run time, never as a literal (`engineering-practices.md`
§ Guards must fail closed: *"A fixture for a secret scanner is built at run
time"*).

| # | At the pin | Function | What a case would catch |
| --- | --- | --- | --- |
| **3.1** | `utils/StringUtil.cpp:357-362`, `:398-403`; tables `:76`, `:93`, `:153`, `:170` | `toUpper`, `toLower` in `es-unit-tests` | **`CHECK(toUpper("\xE1\xBA\xA1") == "\xE1\xBA\xA0")`, `CHECK(toLower("\xEF\xBC\xA1") == "\xEF\xBD\x81")` FAIL at the pin (L-01; R2 § 8)**; a 2-byte French pair PASSes beside them |
| **3.2** | `utils/FileSystemUtil.cpp:1451-1455`, `:1463`; `:1472-1474`, `:1492`, `:1500-1504` | `renameFile`, `copyFile`, `FileSystemUtil.cpp` linked whole (T21's `es-fs-tests` shape) | **`CHECK_FALSE(renameFile(<absent>, <tmp>))`, `CHECK_FALSE(copyFile(<absent>, <tmp>))`; `renameFile(<a>, <existing>, false)` keeps the existing file -- FAIL at the pin (L-03)**; T21's merged fix turns the `renameFile` half green, `copyFile`'s stays this slice's |
| **3.3** | `utils/FileSystemUtil.cpp:1429-1446` | `writeAllText` | **at the pin there is no return to test** (R2 L-04): a text case records `void` and the unchecked `fwrite`/`fclose`; the fix's case `CHECK_FALSE(writeAllText("/dev/full", "x"))` written for whatever the pause rules (T21 PL-20 / #1186) |
| **3.4** | `utils/FileSystemUtil.cpp:1369-1379`, `:1400-1427` | `readAllText`, `readAllLines` | **write `1\n`; `CHECK(readAllText(p) == "1\n")`, `CHECK(readAllLines(p).size() == 1)` FAIL at the pin (L-02)** -- the control T20's `d9afa5c7c` turns green at the integration, never re-fixed here |
| **3.5** | `utils/Platform.cpp:162-164` | the wrap's literal, run by the host's shell | **with a producer that outlives the pipe buffer, `sh -c '((((seq 1 200000 2> /dev/null ; echo $? >&3) \| head -300 > /dev/null) 3>&1) \| (read xs; exit $xs))'; echo $?` printed `141` on the host's `/usr/bin/dash`, `0` wanted (L-05; proof C1, CMD12)**; the same literal with `seq 1 400` (1,492 bytes, held whole by the pipe) printed `0` (proof CMD4) and is recorded as the PASS-at-pin control -- one run is one observation, the 141 timing-dependent in principle; stage A's runs (§ 5); the image's shell on the guest is G-07 |
| **3.6** | `utils/FileSystemUtil.cpp:1758-1798` (`:1773`, `:1775`, `:1788`, `:1797`) | `preloadFileSystemCache` under ASan | **with `ASAN_OPTIONS=detect_stack_use_after_return=1`, call it and return: a stack-use-after-return report at the pin (L-15)**; the fix captures by value |
| **3.7** | `utils/Platform.cpp:853-880` (`:879`) | `runSystemCommand`, lifted as text | **the body returns `0` at `:879` and reads neither `name` nor `window`** (L-13): the rule erratum's proof (`proved: tree`); no caller reads the return (R2 cmd 14) |
| **3.8** | `resources/Font.cpp:107`, `:115-117`, `:420-421`, `:754-757` | `getHeight` (FreeType and renderer stand-ins) | **a positive, not a FAIL**: `h = getHeight(); sizeText(<ASCII 32..126>); CHECK(getHeight() == h)` -- PASS at the pin is L-08's proof against `es-code-traps.md:118` |
| **3.9** | `utils/Platform.cpp:891-905` | `GetShOutput`, extracted | **`GetShOutput("printf '%0300d\n' 0").size()` is 299 at the pin, 300 wanted (L-06)** -- the control for T26's S8, never re-fixed here |
| **3.10** | `utils/StringUtil.cpp:446-804` | `maskSecrets` in `es-unit-tests` (`MaskSecretsTests.cpp` exists) | **a JSON `"token":"<value>"` with a non-placeholder value built at run time keeps its value at the pin (L-14)**; `name: value` and `Authorization: Bearer` the same |
| 3.11 | `resources/TextureData.cpp:615-645`, `:670-725` against `:92-195` | a `san tsan-...` stand-in | one thread `initSVGFromMemory`, the main thread `setMaxSize`: a TSan report at the pin (L-10); `vlc/vlc.h` faked, `nanosvg` from the tree |
| 3.12 | `resources/TextureDataManager.cpp:215-235`, `:252-253`, `:284` | `TextureLoader`'s teardown, with a timeout | construct, set `paused`, destroy: the join does not return inside the timeout (L-11) |
| 3.13 | `utils/FileSystemUtil.cpp:48-341`, `:1122-1147`, `:161-162` | the cache, extracted in T35's `fs_cache`/`fs_exists` shape | a positive: `exists(p)` miss, `p` written by `std::ofstream`, `exists(p, false)` true and then `exists(p)` true (the entry rewritten, L-12); a listing's wildcard then a file written under it: `exists` false without a stat |
| **3.14** | T35's `window-input-tests` case 3.11 at T35's tip (`InputManager.cpp:1187` with `FileSystemUtil.cpp`) | re-run unchanged, never edited (ruling (h)) | **FAIL at the pin** (`RUN window-input-tests: rc 1; [doctest] test cases: 10 \| 3 passed \| 7 failed ...`, T35 `stage-c/build-tests.out:65`, the tail abridged here; R3 § 1.4; proof C8, CMD15); PASS only when the cache's fix or T35's caller fix lands |
| 3.15 | `utils/FileSystemUtil.cpp:1089-1120` | `createDirectory` | two threads create one path: either returns `false` while the directory exists (L-16) |
| 3.16 | `resources/Font.cpp:99`, `:161-165`, `:1238`, `:1255`; `Renderer.cpp:1149` doubled | the scaling, extracted | `getFromTheme(elem{fontPath only}, ..., orig)->getSize() == orig->getSize()` (L-07); `fontScale()` 1.31 under 720 px, 1.5 under 320 (R3 § 4) |
| 3.17 | `resources/Font.cpp:714-752`, `:1044-1078` | `sizeText` against the cache's last vertex (stand-ins) | a substitutable code point measured wider than it is drawn; the newline's advance counted (L-09) |
| 3.18 | `utils/StringUtil.cpp:426-444` | `shellQuote` in `es-unit-tests` | single quotes around the value, `'` escaped, the empty string quoted -- PASS expected, the contract four fixes rest on (R4 item 24) |
| 3.19 | `getEscapedPath` (`FileSystemUtil.cpp`) | linked whole | each of the shell's metacharacters in a ROM name escaped or not; the ones left named (R4 item 15) |
| 3.20 | `getCanonicalPath` (`:726`, T2's line) | linked whole, ASan | a path of more than 32 components: a write past the array at the pin or not (R4 item 16) |
| 3.21 | the relative path (`:986`) | linked whole | `/storage/roms/snes2/a.png` against `/storage/roms/snes` gives `.//a.png` (R4 item 17) |
| 3.22 | `utils/TimeUtil.cpp:514-588` | `LocaleES` and `Settings` doubles | the ten `_("` shapes (`%d d`, `%d h`, `%d mn`, `%d sec`, `never`) at their thresholds; the 12-hour switch read per call |
| 3.23 | `resources/TextureDataManager.cpp:135-170` | `cleanupVRAM`, extracted | eviction from the least recent end until under `MaxVRAM` MiB; non-reloadable and required textures kept (R3 § 3) |
| 3.24 | `utils/Platform.cpp:235-237` | `quitES`, lifted as text | the `new SDL_Event` never freed (L-18); recorded |
| 3.25 | `FileSystemUtil.cpp:331-332` (`shared_mutex`); `ThreadPool.cpp:26`, `:84`, `:91`; `StringListLock.cpp`; `ConcurrentVector.h` | `san()` TSan programs (R3 § 6 item 2) | concurrent `exists` and cache writers; the pool's start and join; the list lock -- each program's first report line, or none |


