package hep.lcio.implementation.sio;

import hep.lcd.io.sio.SIOInputStream;
import hep.lcd.io.sio.SIOOutputStream;

import hep.lcio.event.ParticleID;
import hep.lcio.implementation.event.IParticleID;

import java.io.IOException;

/**
 *
 * @author Tony Johnson
 * @version $Id: SIOParticleID.java,v 1.1 2004-09-13 22:43:09 tonyj Exp $
 */
class SIOParticleID extends IParticleID
{
   SIOParticleID(SIOInputStream in, SIOEvent owner, int flag, int major, int minor) throws IOException
   {
      setParent(owner);
      logLikelihood = in.readFloat();
      type = in.readInt();
      pdg = in.readInt();
      goodnessOfPID = in.readFloat();
      identifier = in.readString();
      int n = in.readInt();
      parameters = new float[n];
      for (int i=0; i<n; i++) parameters[i] = in.readInt();
      in.readPTag(this);
   }

   static void write(ParticleID id, SIOOutputStream out) throws IOException
   {
      if (id instanceof SIOParticleID)
      {
         ((SIOParticleID) id).write(out);
      }
      else
      {
         out.writeFloat(id.getPDG());
         out.writeInt(id.getType());
         out.writeInt(id.getPDG());
         out.writeFloat(id.getGoodnessOfPID());
         out.writeString(id.getIdentifier());
         float[] pars = id.getParameters();
         for (int i=0; i<pars.length; i++) out.writeFloat(pars[i]);
         out.writePTag(id);
      }
   }

   private void write(SIOOutputStream out) throws IOException
   {
      out.writeFloat(logLikelihood);
      out.writeInt(type);
      out.writeInt(pdg);
      out.writeFloat(goodnessOfPID);
      out.writeString(identifier);
      for (int i=0; i<parameters.length; i++) out.writeFloat(parameters[i]);
      out.writePTag(this);
   }
}